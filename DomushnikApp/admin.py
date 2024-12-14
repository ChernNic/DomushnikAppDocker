from django.contrib import admin

# Register your models here.
# DomushnikApp/admin.py

from django.contrib import admin
from .models import (
    Landlord,
    Purpose,
    Address,
    PropertyType,
    Amenity,
    Property,
    PropertyPhoto,
    PropertyFeature,
    Rental,
    RentalApplication,
    Payment,
    NotificationType,
    Notification,
    Backup,
    AdminLog,
    UserProfile
)

admin.site.register(Purpose)
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(PropertyType)
admin.site.register(Amenity)
admin.site.register(Property)
admin.site.register(PropertyPhoto)
admin.site.register(PropertyFeature)
admin.site.register(Rental)
admin.site.register(RentalApplication)
admin.site.register(Payment)
admin.site.register(NotificationType)
admin.site.register(Notification)
admin.site.register(Backup)
admin.site.register(AdminLog)
admin.site.register(Landlord)

