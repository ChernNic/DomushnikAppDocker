from django.db.models import Count
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views import View
from django_filters.views import FilterView
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from DomushnikApp.User.filters import PropertyFilter
from DomushnikApp.User.froms import *
from DomushnikApp.admin_panel.adminViews import PaginationMixin
from DomushnikApp.models import APPLICATION_STATUS_CHOICES, Address, Amenity, Landlord, Payment, Property, PropertyType, Rental, RentalApplication, Review

class CatalogListView(FilterView):
    model = Property
    template_name = 'user/property_catalog.html'
    context_object_name = 'properties'
    filterset_class = PropertyFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['amenity_counts'] = Amenity.objects.annotate(property_count=Count('properties'))
        context['property_type_counts'] = PropertyType.objects.annotate(property_count=Count('properties'))
        context['property_usage_counts'] = Property.objects.values('property_usage').annotate(property_count=Count('id'))
        return context
    


@method_decorator(login_required, name='dispatch')
class PropertyDetailsView(View):
    model = Property
    template_name = 'user/property_item.html'

    def get(self, request, *args, **kwargs):
        try:
            property_id = kwargs.get('pk')
            property_item = self.model.objects.select_related('landlord__landlord_profile', 'landlord__profile', 'address').get(pk=property_id)
        except self.model.DoesNotExist:
            return HttpResponseNotFound("Property not found")

        # Получаем Landlord
        landlord_instance = getattr(property_item.landlord, 'landlord_profile', None)
        reviews = Review.objects.filter(landlord=landlord_instance) if landlord_instance else []

        form = ReviewForm()

        context = {
            'property': property_item,
            'reviews': reviews,
            'review_form': form,
        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        property_id = kwargs.get('pk')
        try:
            property_item = self.model.objects.get(pk=property_id)
        except self.model.DoesNotExist:
            return HttpResponseNotFound("Property not found")

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tenant = request.user.profile

            # Получаем объект Landlord
            landlord_instance = getattr(property_item.landlord, 'landlord_profile', None)
            if not landlord_instance:
                return JsonResponse({'status': 'error', 'message': 'Landlord not found'})

            review.landlord = landlord_instance
            review.save()
            print("Ваш отзыв успешно добавлен.")
            return redirect('property_detail', pk=property_id)

        reviews = Review.objects.filter(landlord=property_item.landlord.landlord_profile)
        context = {
            'property': property_item,
            'reviews': reviews,
            'review_form': form,
        }
        return render(request, self.template_name, context)

    


@login_required
def rent_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)

    # Проверяем, есть ли уже заявка от текущего пользователя на эту собственность
    existing_application = property_instance.applications.filter(tenant=request.user).exists()

    if existing_application:
        return render(request, 'User/rental_application.html', {
            'property': property_instance,
            'application_exists': True
        })

    if request.method == 'POST':
        form = UserRentalApplicationForm(request.POST)
        if form.is_valid():
            rental_application = form.save(commit=False)
            rental_application.tenant = request.user
            rental_application.property = property_instance
            rental_application.status = 'pending'  # Устанавливаем статус "в ожидании"
            rental_application.save()
            return render(request, 'User/rental_application.html', {
                'property': property_instance,
                'application_sent': True
            })
    else:
        form = UserRentalApplicationForm()

    return render(request, 'User/rental_application.html', {
        'property': property_instance,
        'form': form
    })



@login_required
def profile_view(request):
    # Получение профиля пользователя
    profile = request.user.profile
    is_landlord = hasattr(request.user, 'landlord_profile')
    landlord_profile = getattr(request.user, 'landlord_profile', None)

    # Инициализация форм
    form = UserProfileForm(instance=profile)
    landlord_form = LandlordForm(instance=landlord_profile) if is_landlord else LandlordForm()

    if request.method == 'POST':
        # Логика обработки формы профиля
        if 'update_profile' in request.POST:
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен.')
                return redirect('profile')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

        # Логика обработки формы арендодателя
        elif 'update_landlord' in request.POST and is_landlord:
            landlord_form = LandlordForm(request.POST, request.FILES, instance=landlord_profile)
            if landlord_form.is_valid():
                landlord_form.save()
                messages.success(request, 'Информация арендодателя обновлена.')
                return redirect('profile')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

        # Логика обработки формы становления арендодателем
        elif 'become_landlord' in request.POST and not is_landlord:
            landlord_form = LandlordForm(request.POST, request.FILES)
            if landlord_form.is_valid():
                landlord = landlord_form.save(commit=False)
                landlord.user = request.user
                landlord.save()
                messages.success(request, 'Вы успешно стали арендодателем!')
                return redirect('profile')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    # Рендеринг страницы профиля
    return render(request, 'User/profile.html', {
        'form': form,
        'profile': profile,
        'is_landlord': is_landlord,
        'landlord_form': landlord_form,
        'landlord_profile': landlord_profile,
    })




@login_required
def my_applications_view(request):
    status_filter = request.GET.get('status')
    applications = RentalApplication.objects.filter(tenant=request.user)
    if status_filter in dict(APPLICATION_STATUS_CHOICES).keys():
        applications = applications.filter(status=status_filter)

    return render(request, 'user/my_applications.html', {
        'applications': applications,
        'status_filter': status_filter,
        'APPLICATION_STATUS_CHOICES': APPLICATION_STATUS_CHOICES,
    })


@login_required
def property_applications_view(request):
    # Получаем заявки, которые связаны с недвижимостью текущего пользователя
    applications = RentalApplication.objects.filter(property__landlord=request.user)
    is_landlord = hasattr(request.user, 'landlord_profile')

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(RentalApplication, id=application_id, property__landlord=request.user)

        if new_status in dict(application._meta.get_field('status').choices).keys():
            application.status = new_status
            application.save()

            # Если статус заявки "одобрено", создаем аренду
            if new_status == 'approved':
                Rental.objects.create(
                    property=application.property,
                    tenant=application.tenant,
                    start_date=None,  # Можно указать логику для заполнения
                    end_date=None,
                    is_active=False
                )
                print(f"Заявка #{application_id} одобрена, аренда создана.")
            else:
                messages.info(request, f"Статус заявки #{application_id} обновлен на {application.get_status_display()}.")
        else:
            messages.error(request, "Некорректный статус.")

        return redirect('property_applications')

    return render(request, 'user/property_applications.html', {
        'is_landlord': is_landlord,
        'applications': applications,
    })


@login_required
def my_rentals_view(request):
    rentals = Rental.objects.filter(tenant=request.user)

    if request.method == 'POST':
        rental_id = request.POST.get('rental_id')
        rental = get_object_or_404(Rental, id=rental_id, tenant=request.user)

        # Логика "оплаты" аренды
        Payment.objects.create(
            rental=rental,
            amount=rental.property.price_per_month,
            is_paid=True,
        )
        rental.is_active = True
        rental.save()

        print(f"Аренда #{rental_id} успешно оплачена.")
        return redirect('my_rentals')

    return render(request, 'user/my_rentals.html', {
        'rentals': rentals,
    })


@login_required
def my_property_view(request):
    properties = Property.objects.filter(landlord=request.user)
    is_landlord = hasattr(request.user, 'landlord_profile')


    # Добавляем информацию о статусе аренды в свойства
    for property in properties:
        property.is_rented = property.rentals.filter(is_active=True).exists()

    return render(request, 'user/my_property.html', {'properties': properties, 'is_landlord': is_landlord,})


@login_required
def property_add_edit_view(request, pk=None):
    property_instance = get_object_or_404(Property, pk=pk, landlord=request.user) if pk else None

    if request.method == 'POST':
        form = PropertyWithAddressForm(request.POST, request.FILES, instance=property_instance)
        photo_formset = PropertyPhotoFormSet(request.POST, request.FILES, instance=property_instance)

        if form.is_valid() and photo_formset.is_valid():
            # Сохраняем объект Property, но не сохраняем связанные данные
            property_saved = form.save(commit=False)
            property_saved.landlord = request.user

            # Создаем или обновляем объект Address
            address_data = {
                'latitude': form.cleaned_data['latitude'],
                'longitude': form.cleaned_data['longitude'],
                'city': form.cleaned_data['city'],
                'state': form.cleaned_data['state'],
                'country': form.cleaned_data['country'],
                'zip_code': form.cleaned_data['zip_code'],
                'street': form.cleaned_data['street'],
                'house': form.cleaned_data['house'],
            }

            # Если у объекта уже есть связанный адрес, обновляем его
            if property_instance and property_instance.address:
                for field, value in address_data.items():
                    setattr(property_instance.address, field, value)
                property_instance.address.save()
                property_saved.address = property_instance.address
            else:
                # Создаем новый объект Address
                new_address = Address.objects.create(**address_data)
                property_saved.address = new_address

            # Сохраняем Property
            property_saved.save()

            # Сохраняем многие ко многим (удобства)
            form.save_m2m()

            # Сохраняем фотографии
            photo_formset.instance = property_saved
            photo_formset.save()

            messages.success(request, "Недвижимость успешно сохранена.")
            return redirect('my_property')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")

    else:
        form = PropertyWithAddressForm(instance=property_instance)
        photo_formset = PropertyPhotoFormSet(instance=property_instance)

    return render(request, 'user/property_form.html', {
        'form': form,
        'photo_formset': photo_formset,
    })


@login_required
def property_delete_view(request, pk):
    property_instance = get_object_or_404(Property, pk=pk, landlord=request.user)
    if request.method == 'POST':
        property_instance.delete()
        print("Недвижимость успешно удалена.")
        return redirect('my_property')

    return render(request, 'user/property_confirm_delete.html', {'property': property_instance})