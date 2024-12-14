from io import StringIO
import json
import logging
import os
import subprocess
import time
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from DomushnikApp.admin_panel.forms import AdminLogForm, AmenityForm, LandlordForm, ModeratorForm, ModeratorLogForm, NotificationForm, NotificationTypeForm, PaymentForm, PropertyForm, PropertyPhotoFormSet, PropertyFeatureFormSet, AddressForm, PropertyTypeForm, PurposeForm, RentalApplicationForm, RentalForm, ReviewForm, UserProfileForm, UserUpdateForm
from DomushnikApp.models import Address, AdminLog, Amenity, Backup, Landlord, Moderator, ModeratorLog, Notification, NotificationType, Payment, PropertyType, Property, Purpose, Rental, RentalApplication, Review, UserProfile, log_admin_action
from .filters import AddressFilter, AdminLogFilter, AmenityFilter, BackupFilter, LandlordFilter, ModeratorFilter, ModeratorLogFilter, NotificationFilter, NotificationTypeFilter, PaymentFilter, PropertyTypeFilter, PropertyFilter, PurposeFilter, RentalApplicationFilter, RentalFilter, ReviewFilter, UserFilter, UserProfileFilter
from .tables import AddressTable, AdminLogTable, AmenityTable, BackupTable, LandlordTable, ModeratorLogTable, ModeratorTable, NotificationTable, NotificationTypeTable, PaymentTable, PropertyTypeTable, PropertyTable, PurposeTable, RentalApplicationTable, RentalTable, ReviewTable, UserProfileTable, UserTable
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.management import call_command
from django.utils.timezone import now
from django.apps import apps 

class UserContextMixin:
    # Capturing the user for form updates
    def form_valid(self, form):
        print("Вызван метод form_valid") 
        if self.request.user.is_authenticated:
            form.instance._updated_by = self.request.user  # Set the user performing the update
        return super().form_valid(form)

class DeletionLogMixin:
    def form_valid(self, form):
        obj = self.get_object()
        
        # Логируем удаление объекта
        if self.request.user.is_authenticated:
            # Записываем в лог администрирования
            log_admin_action(
                action="Удаление",
                model_name=obj.__class__.__name__,
                instance=obj,
                user=self.request.user
            )
            
            # Логируем информацию о пользователе, который удаляет объект
            obj._deleted_by = self.request.user
            obj.save()

        return super().form_valid(form)
    

class PaginationMixin:
    paginate_by = 10


# Address Views
class AddressListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Address
    table_class = AddressTable
    template_name = "admin/address_list.html"
    filterset_class = AddressFilter


class AddressCreateView(UserContextMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'admin/address_form.html'
    success_url = reverse_lazy('address_list')


class AddressUpdateView(UserContextMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'admin/address_form.html'
    success_url = reverse_lazy('address_list')


class AddressDeleteView(DeletionLogMixin, DeleteView ):
    model = Address
    template_name = 'admin/address_confirm_delete.html'
    success_url = reverse_lazy('address_list')


# PropertyType Views
class PropertyTypeListView(PaginationMixin, SingleTableMixin, FilterView):
    model = PropertyType
    table_class = PropertyTypeTable
    filterset_class = PropertyTypeFilter
    template_name = 'admin/property_type_list.html'


class PropertyTypeCreateView(UserContextMixin, CreateView):
    model = PropertyType
    form_class = PropertyTypeForm
    template_name = 'admin/property_type_form.html'
    success_url = reverse_lazy('propertytype_list')


class PropertyTypeUpdateView(UserContextMixin, UpdateView):
    model = PropertyType
    form_class = PropertyTypeForm
    template_name = 'admin/property_type_form.html'
    success_url = reverse_lazy('propertytype_list')


class PropertyTypeDeleteView(DeleteView, DeletionLogMixin):
    model = PropertyType
    template_name = 'admin/property_type_confirm_delete.html'
    success_url = reverse_lazy('propertytype_list')


# Property Views
class PropertyListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Property
    table_class = PropertyTable
    filterset_class = PropertyFilter
    template_name = 'admin/property_list.html'


class PropertyCreateView(UserContextMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'admin/property_form.html'
    success_url = reverse_lazy('property_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['photo_formset'] = PropertyPhotoFormSet(self.request.POST or None, self.request.FILES or None)
        data['feature_formset'] = PropertyFeatureFormSet(self.request.POST or None)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']
        feature_formset = context['feature_formset']
        if photo_formset.is_valid() and feature_formset.is_valid():
            self.object = form.save()
            photo_formset.instance = self.object
            photo_formset.save()
            feature_formset.instance = self.object
            feature_formset.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class PropertyUpdateView(UserContextMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'admin/property_form.html'
    success_url = reverse_lazy('property_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['photo_formset'] = PropertyPhotoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object)
        data['feature_formset'] = PropertyFeatureFormSet(self.request.POST or None, instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']
        feature_formset = context['feature_formset']
        if photo_formset.is_valid() and feature_formset.is_valid():
            self.object = form.save()
            photo_formset.instance = self.object
            photo_formset.save()
            feature_formset.instance = self.object
            feature_formset.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class PropertyDeleteView(DeleteView, DeletionLogMixin):
    model = Property
    template_name = 'admin/property_confirm_delete.html'
    success_url = reverse_lazy('property_list')
    

# Amenity Views
class AmenityListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Amenity
    table_class = AmenityTable
    filterset_class = AmenityFilter
    template_name = 'admin/amenity_list.html'


class AmenityCreateView(UserContextMixin, CreateView):
    model = Amenity
    form_class = AmenityForm
    template_name = 'admin/amenity_form.html'
    success_url = reverse_lazy('amenity_list')


class AmenityUpdateView(UserContextMixin, UpdateView):
    model = Amenity
    form_class = AmenityForm
    template_name = 'admin/amenity_form.html'
    success_url = reverse_lazy('amenity_list')


class AmenityDeleteView(DeleteView, DeletionLogMixin):
    model = Amenity
    template_name = 'admin/amenity_confirm_delete.html'
    success_url = reverse_lazy('amenity_list')


# Rental Views
class RentalListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Rental
    table_class = RentalTable
    filterset_class = RentalFilter
    template_name = 'admin/rental_list.html'


class RentalCreateView(UserContextMixin, CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'admin/rental_form.html'
    success_url = reverse_lazy('rental_list')


class RentalUpdateView(UserContextMixin, UpdateView):
    model = Rental
    form_class = RentalForm
    template_name = 'admin/rental_form.html'
    success_url = reverse_lazy('rental_list')


class RentalDeleteView(DeleteView, DeletionLogMixin):
    model = Rental
    template_name = 'admin/rental_confirm_delete.html'
    success_url = reverse_lazy('rental_list')


# Payment Views
class PaymentListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Payment
    table_class = PaymentTable
    filterset_class = PaymentFilter
    template_name = 'admin/payment_list.html'


class PaymentCreateView(UserContextMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'admin/payment_form.html'
    success_url = reverse_lazy('payment_list')


class PaymentUpdateView(UserContextMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'admin/payment_form.html'
    success_url = reverse_lazy('payment_list')


class PaymentDeleteView(DeleteView, DeletionLogMixin):
    model = Payment
    template_name = 'admin/payment_confirm_delete.html'
    success_url = reverse_lazy('payment_list')


# RentalApplication Views
class RentalApplicationListView(PaginationMixin, SingleTableMixin, FilterView):
    model = RentalApplication
    table_class = RentalApplicationTable
    filterset_class = RentalApplicationFilter
    template_name = 'admin/rental_application_list.html'


class RentalApplicationCreateView(UserContextMixin, CreateView):
    model = RentalApplication
    form_class = RentalApplicationForm
    template_name = 'admin/rental_application_form.html'
    success_url = reverse_lazy('rental_application_list')


class RentalApplicationUpdateView(UserContextMixin, UpdateView):
    model = RentalApplication
    form_class = RentalApplicationForm
    template_name = 'admin/rental_application_form.html'
    success_url = reverse_lazy('rental_application_list')


class RentalApplicationDeleteView(DeleteView, DeletionLogMixin):
    model = RentalApplication
    template_name = 'admin/rental_application_confirm_delete.html'
    success_url = reverse_lazy('rental_application_list')


# NotificationType Views
class NotificationTypeListView(PaginationMixin, SingleTableMixin, FilterView):
    model = NotificationType
    table_class = NotificationTypeTable
    filterset_class = NotificationTypeFilter
    template_name = 'admin/notification_type_list.html'


class NotificationTypeCreateView(UserContextMixin, CreateView):
    model = NotificationType
    form_class = NotificationTypeForm
    template_name = 'admin/notification_type_form.html'
    success_url = reverse_lazy('notification_type_list')


class NotificationTypeUpdateView(UserContextMixin, UpdateView):
    model = NotificationType
    form_class = NotificationTypeForm
    template_name = 'admin/notification_type_form.html'
    success_url = reverse_lazy('notification_type_list')


class NotificationTypeDeleteView(DeleteView, DeletionLogMixin):
    model = NotificationType
    template_name = 'admin/notification_type_confirm_delete.html'
    success_url = reverse_lazy('notification_type_list')


# Notification Views
class NotificationListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Notification
    table_class = NotificationTable
    filterset_class = NotificationFilter
    template_name = 'admin/notification_list.html'


class NotificationCreateView(UserContextMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'admin/notification_form.html'
    success_url = reverse_lazy('notification_list')


class NotificationUpdateView(UserContextMixin, UpdateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'admin/notification_form.html'
    success_url = reverse_lazy('notification_list')


class NotificationDeleteView(DeleteView, DeletionLogMixin):
    model = Notification
    template_name = 'admin/notification_confirm_delete.html'
    success_url = reverse_lazy('notification_list')


# Purpose Views
class PurposeListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Purpose
    table_class = PurposeTable
    filterset_class = PurposeFilter
    template_name = 'admin/purpose_list.html'


class PurposeCreateView(UserContextMixin, CreateView):
    model = Purpose
    form_class = PurposeForm
    template_name = 'admin/purpose_form.html'
    success_url = reverse_lazy('purpose_list')


class PurposeUpdateView(UserContextMixin, UpdateView):
    model = Purpose
    form_class = PurposeForm
    template_name = 'admin/purpose_form.html'
    success_url = reverse_lazy('purpose_list')


class PurposeDeleteView(DeleteView, DeletionLogMixin):
    model = Purpose
    template_name = 'admin/purpose_confirm_delete.html'
    success_url = reverse_lazy('purpose_list')


# AdminLog Views
class AdminLogListView(PaginationMixin, SingleTableMixin, FilterView):
    model = AdminLog
    table_class = AdminLogTable
    filterset_class = AdminLogFilter
    template_name = 'admin/admin_log_list.html'


class AdminLogCreateView(UserContextMixin, CreateView):
    model = AdminLog
    form_class = AdminLogForm
    template_name = 'admin/admin_log_form.html'
    success_url = reverse_lazy('admin_log_list')


class AdminLogUpdateView(UserContextMixin, UpdateView):
    model = AdminLog
    form_class = AdminLogForm
    template_name = 'admin/admin_log_form.html'
    success_url = reverse_lazy('admin_log_list')


class AdminLogDeleteView(DeleteView, DeletionLogMixin):
    model = AdminLog
    template_name = 'admin/admin_log_confirm_delete.html'
    success_url = reverse_lazy('admin_log_list')


# ModeratorLog Views
class ModeratorLogListView(PaginationMixin, SingleTableMixin, FilterView):
    model = ModeratorLog
    table_class = ModeratorLogTable
    filterset_class = ModeratorLogFilter
    template_name = 'admin/moderator_log_list.html'


class ModeratorLogCreateView(UserContextMixin, CreateView):
    model = ModeratorLog
    form_class = ModeratorLogForm
    template_name = 'admin/moderator_log_form.html'
    success_url = reverse_lazy('moderator_log_list')


class ModeratorLogUpdateView(UserContextMixin, UpdateView):
    model = ModeratorLog
    form_class = ModeratorLogForm
    template_name = 'admin/moderator_log_form.html'
    success_url = reverse_lazy('moderator_log_list')


class ModeratorLogDeleteView(DeleteView, DeletionLogMixin):
    model = ModeratorLog
    template_name = 'admin/moderator_log_confirm_delete.html'
    success_url = reverse_lazy('moderator_log_list')


# List View
class ReviewListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Review
    table_class = ReviewTable
    filterset_class = ReviewFilter
    template_name = 'admin/review_list.html'

# Create View
class ReviewCreateView(UserContextMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'admin/review_form.html'
    success_url = reverse_lazy('review_list')

# Update View
class ReviewUpdateView(UserContextMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'admin/review_form.html'
    success_url = reverse_lazy('review_list')

# Delete View
class ReviewDeleteView(DeleteView, DeletionLogMixin):
    model = Review
    template_name = 'admin/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')


# List View
class ModeratorListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Moderator
    table_class = ModeratorTable
    filterset_class = ModeratorFilter  # Use the filter here
    template_name = 'admin/moderator_list.html'
    
# Create View
class ModeratorCreateView(UserContextMixin, CreateView):
    model = Moderator
    form_class = ModeratorForm
    template_name = 'admin/moderator_form.html'
    success_url = reverse_lazy('moderator_list')

# Update View
class ModeratorUpdateView(UserContextMixin, UpdateView):
    model = Moderator
    form_class = ModeratorForm
    template_name = 'admin/moderator_form.html'
    success_url = reverse_lazy('moderator_list')

# Delete View
class ModeratorDeleteView(DeleteView, DeletionLogMixin):
    model = Moderator
    template_name = 'admin/moderator_confirm_delete.html'
    success_url = reverse_lazy('moderator_list')


# List View with filtering
class UserProfileListView(PaginationMixin, SingleTableMixin, FilterView):
    model = UserProfile
    table_class = UserProfileTable
    filterset_class = UserProfileFilter  # Using filter
    template_name = 'admin/userprofile_list.html'

# Create View
class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'admin/userprofile_form.html'
    success_url = reverse_lazy('userprofile_list')

    def form_valid(self, form):
        # Set the user to the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

# Update View
class UserProfileUpdateView(UserContextMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'admin/userprofile_form.html'
    success_url = reverse_lazy('userprofile_list')

# Delete View
class UserProfileDeleteView(DeleteView, DeletionLogMixin):
    model = UserProfile
    template_name = 'admin/userprofile_confirm_delete.html'
    success_url = reverse_lazy('userprofile_list')


# List View with filtering
class LandlordListView(PaginationMixin, SingleTableMixin, FilterView):
    model = Landlord
    table_class = LandlordTable
    filterset_class = LandlordFilter  # Using filter
    template_name = 'admin/landlord_list.html'

# Create View
class LandlordCreateView(UserContextMixin, CreateView):
    model = Landlord
    form_class = LandlordForm
    template_name = 'admin/landlord_form.html'
    success_url = reverse_lazy('landlord_list')

# Update View
class LandlordUpdateView(UserContextMixin, UpdateView):
    model = Landlord
    form_class = LandlordForm
    template_name = 'admin/landlord_form.html'
    success_url = reverse_lazy('landlord_list')

# Delete View
class LandlordDeleteView(DeleteView, DeletionLogMixin):
    model = Landlord
    template_name = 'admin/landlord_confirm_delete.html'
    success_url = reverse_lazy('landlord_list')


class UserListView(PaginationMixin, SingleTableMixin, FilterView):
    model = User
    table_class = UserTable
    filterset_class = UserFilter
    template_name = 'admin/user_list.html'
    paginate_by = 10  # Optional: number of users per page


class UserSetActiveView(View):
    """
    View to toggle the active status of a user.
    """
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active  # Toggle the active status
        user.save()
        return redirect('user_list')  # Redirect back to the user list page
    

class UserUpdateView(UserContextMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'admin/user_form.html'
    success_url = reverse_lazy('user_list')  # Redirect to the user list after successful update


class BackupListView(SingleTableMixin, FilterView):
    model = Backup
    table_class = BackupTable  # Определите таблицу в tables.py
    filterset_class = BackupFilter  # Определите фильтр в filters.py
    template_name = 'admin/backup_list.html'
    paginate_by = 10  # Количество элементов на странице


class BackupCreateView(CreateView):
    model = Backup
    fields = []
    template_name = 'admin/backup_form.html'
    success_url = reverse_lazy('backup_list')

    def form_valid(self, form):
        try:
            app_name = "DomushnikApp"
            backup_dir = 'backups'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            filename = f"backup_{now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(backup_dir, filename)

            # Создание бэкапа
            os.system(f'python manage.py dumpdata {app_name} --indent 2 > {file_path} ')

            # Сохраняем путь в экземпляре формы
            form.instance.file_path = file_path

            # Вывод сообщения об успехе
            messages.success(self.request, "Бэкап успешно создан.")
        except Exception as e:
            messages.error(self.request, f"Ошибка создания бэкапа: {str(e)}")
            return self.form_invalid(form)

        return super().form_valid(form)


class BackupDeleteView(DeleteView):
    model = Backup
    template_name = 'admin/backup_confirm_delete.html'
    success_url = reverse_lazy('backup_list')

    def delete(self, request, *args, **kwargs):
        backup = get_object_or_404(Backup, pk=kwargs['pk'])
        try:
            if os.path.exists(backup.file_path):
                os.remove(backup.file_path)
            backup.delete()
            messages.success(request, f"Бэкап {backup.file_path} успешно удален.")
        except Exception as e:
            messages.error(request, f"Ошибка удаления: {str(e)}")
        return super().delete(request, *args, **kwargs)
    


class BackupRestoreView(View):
    def get(self, request, *args, **kwargs):
        backup = get_object_or_404(Backup, pk=kwargs.get('pk'))
        return render(request, 'admin/backup_restore.html', {'backup': backup})

    def post(self, request, *args, **kwargs):
        backup = get_object_or_404(Backup, pk=kwargs.get('pk'))
        try:
            if not os.path.exists(backup.file_path):
                messages.error(request, f"Файл резервной копии {backup.file_path} не найден.")
                return redirect('backup_list')

            # Использование call_command для восстановления данных
            with open(backup.file_path, 'r') as file:
                call_command('loaddata', file.name)

            messages.success(request, f"Данные успешно восстановлены из {backup.file_path}.")
        except Exception as e:
            messages.error(request, f"Ошибка восстановления данных: {str(e)}")
        return redirect('backup_list')
    

class ExportModelDataView(View):
    def get(self, request, model_name):
        try:
            # Проверяем, существует ли модель
            from django.apps import apps
            model = apps.get_model(app_label='DomushnikApp', model_name=model_name)

            if not model:
                return JsonResponse({'error': f"Модель {model_name} не найдена."}, status=404)

            # Генерация JSON
            output = StringIO()
            call_command('dumpdata', f'{model._meta.app_label}.{model._meta.model_name}', indent=2, stdout=output)

            # Подготовка JSON для отправки
            response = HttpResponse(output.getvalue(), content_type='application/json')
            response['Content-Disposition'] = f'attachment; filename="{model_name}_data.json"'

            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class ImportModelDataView(View):
    def post(self, request, model_name):
        try:
            file = request.FILES.get('file')
            if not file:
                return JsonResponse({'message': 'Файл не предоставлен.'}, status=400)

            # Получаем модель по имени
            model = apps.get_model(app_label='DomushnikApp', model_name=model_name)
            if not model:
                return JsonResponse({'error': f"Модель {model_name} не найдена."}, status=404)

            data = json.load(file)

            from django.contrib.auth.models import User
            from DomushnikApp.models import Address, PropertyType, Amenity

            for item in data:
                fields = item['fields']

                # Обработка landlord (замена ID на экземпляр User)
                if 'landlord' in fields:
                    try:
                        fields['landlord'] = User.objects.get(pk=fields['landlord'])
                    except User.DoesNotExist:
                        return JsonResponse({'error': f"Пользователь с ID {fields['landlord']} не найден."}, status=400)

                # Обработка address (замена ID на экземпляр Address)
                if 'address' in fields and fields['address']:
                    try:
                        fields['address'] = Address.objects.get(pk=fields['address'])
                    except Address.DoesNotExist:
                        return JsonResponse({'error': f"Адрес с ID {fields['address']} не найден."}, status=400)

                # Обработка type (замена ID на экземпляр PropertyType)
                if 'type' in fields:
                    try:
                        fields['type'] = PropertyType.objects.get(pk=fields['type'])
                    except PropertyType.DoesNotExist:
                        return JsonResponse({'error': f"Тип недвижимости с ID {fields['type']} не найден."}, status=400)

                # Извлекаем IDs для amenities
                amenities_ids = fields.pop('amenities', [])

                # Создаем объект
                obj = model.objects.create(**fields)

                # Устанавливаем ManyToManyField для amenities
                if amenities_ids:
                    amenities = Amenity.objects.filter(pk__in=amenities_ids)
                    obj.amenities.set(amenities)

            # Возврат на предыдущую страницу или другая логика
            messages.success(request, f'Импорт данных для {model_name} завершен.')
            return redirect(f'{model_name.lower()}_list')  # Укажите имя URL, куда нужно перенаправить

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
