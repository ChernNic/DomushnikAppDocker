import django_filters
from django import forms
from DomushnikApp.models import *

class AddressFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',  # Поиск по названию города (игнорируя регистр)
        label="Город",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Применяем стиль
    )
    country = django_filters.CharFilter(
        field_name='country',
        lookup_expr='icontains',  # Поиск по названию страны (игнорируя регистр)
        label="Страна",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Применяем стиль
    )
    zip_code = django_filters.CharFilter(
        field_name='zip_code',
        lookup_expr='icontains',  # Поиск по индексу
        label="Индекс",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Применяем стиль
    )

    class Meta:
        model = Address
        fields = ['city', 'country', 'zip_code']


class PropertyTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',  # Поиск по названию (независимо от регистра)
        label="Название",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains',  # Поиск по описанию
        label="Описание",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = PropertyType
        fields = ['name', 'description']


class PropertyFilter(django_filters.FilterSet):
    landlord = django_filters.CharFilter(
        field_name='landlord__username',
        lookup_expr='icontains',
        label="Арендодатель",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    type = django_filters.CharFilter(
        field_name='type__name',
        lookup_expr='icontains',
        label="Тип",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    address = django_filters.CharFilter(
        field_name='address__city',
        lookup_expr='icontains',
        label="Город",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Property
        fields = ['landlord', 'type', 'address', 'availability_status']



class AmenityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label="Название удобства",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Amenity
        fields = ['name']



class RentalFilter(django_filters.FilterSet):
    property = django_filters.ModelChoiceFilter(
        queryset=Property.objects.all(),
        label="Недвижимость",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    tenant = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Арендатор",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    start_date = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte',
        label="Дата начала (с)",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    end_date = django_filters.DateFilter(
        field_name='end_date',
        lookup_expr='lte',
        label="Дата окончания (до)",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    is_active = django_filters.BooleanFilter(
        field_name='is_active',
        label="Активный",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Rental
        fields = ['property', 'tenant', 'start_date', 'end_date', 'is_active']


class PaymentFilter(django_filters.FilterSet):
    rental = django_filters.CharFilter(
        field_name='rental__property__address__city',
        lookup_expr='icontains',
        label="Город",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    amount = django_filters.RangeFilter(
        field_name='amount',
        label="Сумма",
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control'}),
    )
    is_paid = django_filters.BooleanFilter(
        field_name='is_paid',
        label="Оплачено",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Payment
        fields = ['rental', 'amount', 'is_paid']


class RentalApplicationFilter(django_filters.FilterSet):
    tenant = django_filters.CharFilter(
        field_name='tenant__username',
        lookup_expr='icontains',
        label="Арендатор",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    property = django_filters.CharFilter(
        field_name='property__address__city',
        lookup_expr='icontains',
        label="Город недвижимости",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=APPLICATION_STATUS_CHOICES,
        label="Статус",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = RentalApplication
        fields = ['tenant', 'property', 'status']


class NotificationTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',  # Search by name (case insensitive)
        label="Название типа",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = NotificationType
        fields = ['name']


class NotificationFilter(django_filters.FilterSet):
    notification_type = django_filters.ModelChoiceFilter(
        queryset=NotificationType.objects.all(),
        label="Тип уведомления",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    recipient = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label="Получатель",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    content = django_filters.CharFilter(
        field_name='content',
        lookup_expr='icontains',  # Search by content (case insensitive)
        label="Содержание",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    sent_date = django_filters.DateFilter(
        field_name='sent_date',
        lookup_expr='gte',  # Search for notifications sent after or on a specific date
        label="Дата отправки",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = Notification
        fields = ['notification_type', 'recipient', 'content', 'sent_date']


class PurposeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',  # Search by name (case-insensitive)
        label="Название",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Purpose
        fields = ['name']


class AdminLogFilter(django_filters.FilterSet):
    admin = django_filters.CharFilter(
        field_name='admin__username',
        lookup_expr='icontains',  # Search by admin's username
        label="Администратор",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    action = django_filters.CharFilter(
        field_name='action',
        lookup_expr='icontains',  # Search by action text
        label="Действие",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    action_date = django_filters.DateFromToRangeFilter(
        field_name='action_date',
        label="Дата действия",
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = AdminLog
        fields = ['admin', 'action', 'action_date']


class ModeratorLogFilter(django_filters.FilterSet):
    moderator = django_filters.CharFilter(
        field_name='moderator__username',
        lookup_expr='icontains',  # Search by moderator's username
        label="Модератор",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    action = django_filters.CharFilter(
        field_name='action',
        lookup_expr='icontains',  # Search by action text
        label="Действие",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    action_date = django_filters.DateFromToRangeFilter(
        field_name='action_date',
        label="Дата действия",
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = ModeratorLog
        fields = ['moderator', 'action', 'action_date']


class ReviewFilter(django_filters.FilterSet):
    landlord = django_filters.CharFilter(
        field_name='landlord__user__first_name',
        lookup_expr='icontains',
        label="Арендодатель",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    tenant = django_filters.CharFilter(
        field_name='tenant__first_name',
        lookup_expr='icontains',
        label="Арендатор",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    rating = django_filters.RangeFilter(
        field_name='rating',
        label="Рейтинг",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Review
        fields = ['landlord', 'tenant', 'rating']


class ModeratorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        field_name='user__first_name',
        lookup_expr='icontains',
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = django_filters.CharFilter(
        field_name='user__last_name',
        lookup_expr='icontains',
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Moderator
        fields = ['first_name', 'last_name']


class UserProfileFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains',
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = django_filters.CharFilter(
        field_name='first_name',
        lookup_expr='icontains',
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = django_filters.CharFilter(
        field_name='last_name',
        lookup_expr='icontains',
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name']


class LandlordFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains',
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = django_filters.CharFilter(
        field_name='first_name',
        lookup_expr='icontains',
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = django_filters.CharFilter(
        field_name='last_name',
        lookup_expr='icontains',
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    company_name = django_filters.CharFilter(
        field_name='company_name',
        lookup_expr='icontains',
        label="Компания",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    rating = django_filters.RangeFilter(
        field_name='rating',
        label="Рейтинг",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Landlord
        fields = ['username', 'first_name', 'last_name', 'company_name', 'rating']



class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name='username',
        lookup_expr='icontains',
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label="Электронная почта",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    is_active = django_filters.BooleanFilter(
        field_name='is_active',
        label="Активен",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']


class BackupFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Дата создания"
    )
    file_path = django_filters.CharFilter(
        field_name='file_path',
        lookup_expr='icontains',
        label="Путь к файлу",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Backup
        fields = ['created_at', 'file_path']