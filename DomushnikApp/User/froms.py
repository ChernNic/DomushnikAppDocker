from django import forms
from DomushnikApp.models import Address, Landlord, Property, PropertyPhoto, RentalApplication, Purpose, Review, UserProfile

class UserRentalApplicationForm(forms.ModelForm):
    class Meta:
        model = RentalApplication
        fields = ['purpose', 'specific_requirements']  # Добавлено поле purpose
        labels = {
            'purpose': 'Назначение',
            'specific_requirements': 'Комментарий',
        }
        widgets = {
            'purpose': forms.Select(attrs={
                'class': 'form-control',
            }),
            'specific_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш комментарий',
                'rows': 4,
            }),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'avatar', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о себе'
            }),
        }


class LandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = ['is_legal_entity', 'company_name', 'company_logo']
        widgets = {
            'company_logo': forms.FileInput(attrs={
                'class': 'form-control-file'
            }),
                    }
        

class PropertyWithAddressForm(forms.ModelForm):
    latitude = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Широта',
            'readonly': 'readonly',
        }),
        label='Широта'
    )
    longitude = forms.DecimalField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Долгота',
            'readonly': 'readonly',
        }),
        label='Долгота'
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите город'
        }),
        label='Город'
    )
    state = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите область'
        }),
        label='Область'
    )
    country = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите страну'
        }),
        label='Страна'
    )
    zip_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите почтовый индекс'
        }),
        label='Почтовый индекс'
    )
    street = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите улицу'
        }),
        label='Улица'
    )
    house = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите номер дома'
        }),
        label='Дом'
    )

    class Meta:
        model = Property
        fields = [
            'property_name', 'type', 'price_per_month', 'area', 'number_of_rooms',
            'furnished', 'floor', 'total_floors', 'year_built', 'heating_type',
            'availability_status', 'parking', 'balcony', 'pets_allowed',
            'internet_access', 'property_condition', 'property_usage',
            'energy_efficiency_class', 'description', 'amenities'
        ]
        widgets = {
            'property_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название недвижимости'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price_per_month': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену за месяц'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите площадь в м²'
            }),
            'number_of_rooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество комнат'
            }),
            'furnished': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'floor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите этаж'
            }),
            'total_floors': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите общее количество этажей'
            }),
            'year_built': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите год постройки'
            }),
            'heating_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'availability_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'parking': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'balcony': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'pets_allowed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'internet_access': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'property_condition': forms.Select(attrs={
                'class': 'form-control'
            }),
            'property_usage': forms.Select(attrs={
                'class': 'form-control'
            }),
            'energy_efficiency_class': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите описание'
            }),
            'amenities': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
        }


PropertyPhotoFormSet = forms.inlineformset_factory(
    Property,
    PropertyPhoto,
    fields=['photo', 'description'],
    extra=3,  # Количество дополнительных пустых форм
    can_delete=True,
    widgets={
        'photo': forms.FileInput(attrs={
            'class': 'form-control-file',
        }),
        'description': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Описание фотографии (необязательно)'
        }),
    }
)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Рейтинг',
            'comment': 'Комментарий'
        }
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 5,
                'step': 0.1,
                'placeholder': 'Оценка от 0 до 5'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш отзыв',
                'rows': 3
            }),
        }

