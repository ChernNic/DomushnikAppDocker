from django import forms
from django.forms import inlineformset_factory
from DomushnikApp.models import *

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['latitude', 'longitude', 'city', 'state', 'country', 'zip_code', 'street', 'house']
        widgets = {
            'latitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'house': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PropertyTypeForm(forms.ModelForm):
    class Meta:
        model = PropertyType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'property_name','landlord', 'type', 'address', 'price_per_month', 'area', 'number_of_rooms', 'furnished',
            'floor', 'total_floors', 'year_built', 'heating_type', 'availability_status', 'parking',
            'balcony', 'pets_allowed', 'internet_access', 'property_condition', 'property_usage',
            'energy_efficiency_class', 'description', 'amenities'
        ]
        widgets = {
            'property_name': forms.TextInput(attrs={'class': 'form-control'}),
            'landlord': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Select(attrs={'class': 'form-control'}),
            'price_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'furnished': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-control'}),
            'heating_type': forms.Select(attrs={'class': 'form-control'}),
            'availability_status': forms.Select(attrs={'class': 'form-control'}),
            'parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'balcony': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pets_allowed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'internet_access': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'property_condition': forms.Select(attrs={'class': 'form-control'}),
            'property_usage': forms.Select(attrs={'class': 'form-control'}),
            'energy_efficiency_class': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'amenities': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class PropertyPhotoForm(forms.ModelForm):
    class Meta:
        model = PropertyPhoto
        fields = ['photo', 'description']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}), 
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PropertyFeatureForm(forms.ModelForm):
    class Meta:
        model = PropertyFeature
        fields = ['feature_name', 'feature_value']
        widgets = {
            'feature_name': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_value': forms.TextInput(attrs={'class': 'form-control'}),
        }

PropertyPhotoFormSet = inlineformset_factory(
    Property, PropertyPhoto, form=PropertyPhotoForm, extra=1, can_delete=True
)

PropertyFeatureFormSet = inlineformset_factory(
    Property, PropertyFeature, form=PropertyFeatureForm, extra=1, can_delete=True
)


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['property', 'tenant', 'start_date', 'end_date', 'is_active']
        widgets = {
            'property': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['rental', 'amount', 'is_paid']
        widgets = {
            'rental': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RentalApplicationForm(forms.ModelForm):
    class Meta:
        model = RentalApplication
        fields = ['tenant', 'property', 'status', 'purpose', 'specific_requirements']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'property': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'purpose': forms.Select(attrs={'class': 'form-control'}),
            'specific_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class NotificationTypeForm(forms.ModelForm):
    class Meta:
        model = NotificationType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['notification_type', 'recipient', 'content']
        widgets = {
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'recipient': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AdminLogForm(forms.ModelForm):
    class Meta:
        model = AdminLog
        fields = ['admin', 'action']
        widgets = {
            'admin': forms.Select(attrs={'class': 'form-control'}),
            'action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ModeratorLogForm(forms.ModelForm):
    class Meta:
        model = ModeratorLog
        fields = ['moderator', 'action']
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ReviewForm(forms.ModelForm):
    template_name = "form_snippet.html"
    class Meta:
        model = Review
        fields = ['landlord', 'tenant', 'rating', 'comment']
        widgets = {
            'landlord': forms.Select(attrs={'class': 'form-control'}),
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Moderator
        fields = ['user']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
        }


class UserProfileForm(forms.ModelForm):
    # Replace username field with a ModelChoiceField to select an existing User
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Пользователь'
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'phone_number', 'avatar']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with initial values from the selected User model if available.
        This is useful when updating an existing profile.
        """
        user_profile = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user_profile and user_profile.user:
            self.fields['user'].initial = user_profile.user
            self.fields['first_name'].initial = user_profile.user.first_name
            self.fields['last_name'].initial = user_profile.user.last_name
            self.fields['phone_number'].initial = user_profile.phone_number
            self.fields['avatar'].initial = user_profile.avatar

    def save(self, commit=True):
        """
        Override save to handle saving both UserProfile and related User instance.
        """
        user_profile = super().save(commit=False)

        # Set the user instance from the selected user (not create a new one)
        if user_profile.user:
            user_profile.user.first_name = self.cleaned_data.get('first_name', user_profile.user.first_name)
            user_profile.user.last_name = self.cleaned_data.get('last_name', user_profile.user.last_name)
            user_profile.user.save()

        if commit:
            user_profile.save()
        return user_profile


class LandlordForm(forms.ModelForm):
    # Adding user selection field
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Retrieve all users from the User model
        required=True,  # Ensure this field is required
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Пользователь'
    )
    rating = forms.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01, 'min': 0, 'max': 5}),
        label="Рейтинг"
    )
    is_legal_entity = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Юридическое лицо "
    )
    company_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Название компании"
    )
    company_logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="Лого компании"
    )

    class Meta:
        model = Landlord
        fields = ['user', 'rating', 'is_legal_entity', 'company_name', 'company_logo']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
