import django_filters
from DomushnikApp.models import Property, Amenity, PropertyType, Landlord, PROPERTY_USAGE_CHOICES
from django.contrib.auth.models import User

class PropertyFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(
        field_name='address__street',
        lookup_expr='icontains',
        label="Адрес",
        method='filter_address'  # Используем метод для обработки пустых значений
    )
    price_per_month_min = django_filters.NumberFilter(
        field_name='price_per_month',
        lookup_expr='gte',
        label="Минимальная цена"
    )
    price_per_month_max = django_filters.NumberFilter(
        field_name='price_per_month',
        lookup_expr='lte',
        label="Максимальная цена"
    )
    amenities = django_filters.ModelMultipleChoiceFilter(
        field_name='amenities',
        queryset=Amenity.objects.all(),
        widget=django_filters.widgets.CSVWidget(),
        label="Удобства"
    )
    type = django_filters.ModelChoiceFilter(
        field_name='type',
        queryset=PropertyType.objects.all(),
        label="Тип недвижимости"
    )
    property_usage = django_filters.ChoiceFilter(
        field_name='property_usage',
        choices=PROPERTY_USAGE_CHOICES,
        label="Назначение"
    )
    landlord = django_filters.ModelChoiceFilter(
        field_name='landlord',  # Поле связано с моделью User напрямую
        queryset=User.objects.all(),  # Выбор всех пользователей
        label="Арендодатель"
    )

    class Meta:
        model = Property
        fields = ['address', 'price_per_month_min', 'price_per_month_max', 'amenities', 'type', 'property_usage', 'landlord']

    def filter_address(self, queryset, name, value):
        """Проверяем, что поле не пустое перед фильтрацией"""
        if value:
            return queryset.filter(**{name: value})
        return queryset
