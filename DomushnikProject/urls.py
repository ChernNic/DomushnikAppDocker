from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib import admin
from DomushnikApp.Auth.AuthView import (
    RegisterView,
    LoginView,
)
from django.contrib.auth import views as auth_views

from DomushnikApp.User.view import *
from DomushnikApp.admin_panel.adminViews import *

# Функция-заглушка для пустышек
def placeholder_view(request):
    return render(request, 'user/property_catalog.html.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    path('', CatalogListView.as_view(), name='home'),
    
    path('catalog/', CatalogListView.as_view(), name='catalog_list'),
    path('catalog/<int:pk>/', PropertyDetailsView.as_view(), name='property_detail'),
    path('catalog/<int:pk>/rent_property/', rent_property, name='rent_property'),

    path('profile/', profile_view, name='profile'),
    path('my-rentals/', my_rentals_view, name='my_rentals'),
    path('my-applications/', my_applications_view, name='my_applications'),
    path('applications-for-property/', property_applications_view, name='property_applications'),
    path('my_property/', my_property_view, name='my_property'),
    path('my_property/add/', property_add_edit_view, name='my_property_add'),
    path('my_property/edit/<int:pk>/', property_add_edit_view, name='my_property_edit'),
    path('my_property/delete/<int:pk>/', property_delete_view, name='my_property_delete'),


    path('export/<str:model_name>/', ExportModelDataView.as_view(), name='export_model_data'),
    path('import/<str:model_name>/', ImportModelDataView.as_view(), name='import_model_data'),

    # Адреса
    path('admin-panel/addresses/', AddressListView.as_view(), name='address_list'),
    path('admin-panel/addresses/add/', AddressCreateView.as_view(), name='address_add'),
    path('admin-panel/addresses/<int:pk>/edit/', AddressUpdateView.as_view(), name='address_edit'),
    path('admin-panel/addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name='address_delete'),

    # Типы недвижимости
    path('admin-panel/property-types/', PropertyTypeListView.as_view(), name='propertytype_list'),
    path('admin-panel/property-types/add/', PropertyTypeCreateView.as_view(), name='propertytype_add'),
    path('admin-panel/property-types/<int:pk>/edit/', PropertyTypeUpdateView.as_view(), name='propertytype_edit'),
    path('admin-panel/property-types/<int:pk>/delete/', PropertyTypeDeleteView.as_view(), name='propertytype_delete'),

    # Удобства
    path('admin-panel/amenities/', AmenityListView.as_view(), name='amenity_list'),
    path('admin-panel/amenities/add/', AmenityCreateView.as_view(), name='amenity_add'),
    path('admin-panel/amenities/<int:pk>/edit/', AmenityUpdateView.as_view(), name='amenity_edit'),
    path('admin-panel/amenities/<int:pk>/delete/', AmenityDeleteView.as_view(), name='amenity_delete'),

    # Недвижимость
    path('admin-panel/properties/', PropertyListView.as_view(), name='property_list'),
    path('admin-panel/properties/add/', PropertyCreateView.as_view(), name='property_add'),
    path('admin-panel/properties/<int:pk>/edit/', PropertyUpdateView.as_view(), name='property_edit'),
    path('admin-panel/properties/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),

    # Аренда
    path('admin-panel/rentals/', RentalListView.as_view(), name='rental_list'),
    path('admin-panel/rentals/add/', RentalCreateView.as_view(), name='rental_add'),
    path('admin-panel/rentals/<int:pk>/edit/', RentalUpdateView.as_view(), name='rental_edit'),
    path('admin-panel/rentals/<int:pk>/delete/', RentalDeleteView.as_view(), name='rental_delete'),

    # Заявки на аренду
    path('admin-panel/rental-applications/', RentalApplicationListView.as_view(), name='rental_application_list'),
    path('admin-panel/rental-applications/add/', RentalApplicationCreateView.as_view(), name='rental_application_add'),
    path('admin-panel/rental-applications/<int:pk>/edit/', RentalApplicationUpdateView.as_view(), name='rentalapplication_edit'),
    path('admin-panel/rental-applications/<int:pk>/delete/', RentalApplicationDeleteView.as_view(), name='rentalapplication_delete'),

    # Платежи
    path('admin-panel/payments/', PaymentListView.as_view(), name='payment_list'),
    path('admin-panel/payments/add/', PaymentCreateView.as_view(), name='payment_add'),
    path('admin-panel/payments/<int:pk>/edit/', PaymentUpdateView.as_view(), name='payment_edit'),
    path('admin-panel/payments/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),

    # Типы уведомлений
    path('admin-panel/notification-types/', NotificationTypeListView.as_view(), name='notification_type_list'),
    path('admin-panel/notification-types/add/', NotificationTypeCreateView.as_view(), name='notificationtype_add'),
    path('admin-panel/notification-types/<int:pk>/edit/', NotificationTypeUpdateView.as_view(), name='notificationtype_edit'),
    path('admin-panel/notification-types/<int:pk>/delete/', NotificationTypeDeleteView.as_view(), name='notificationtype_delete'),

    # Уведомления
    path('admin-panel/notifications/', NotificationListView.as_view(), name='notification_list'),
    path('admin-panel/notifications/add/', NotificationCreateView.as_view(), name='notification_add'),
    path('admin-panel/notifications/<int:pk>/edit/', NotificationUpdateView.as_view(), name='notification_edit'),
    path('admin-panel/notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification_delete'),

    # Резервные копии
    path('admin-panel/backups/', BackupListView.as_view(), name='backup_list'),
    path('admin-panel/backups/add/', BackupCreateView.as_view(), name='backup_add'),
    path('admin-panel/backups/<int:pk>/restore/', BackupRestoreView.as_view(), name='backup_restore'),
    path('admin-panel/backups/<int:pk>/delete/', BackupDeleteView.as_view(), name='backup_delete'),

    # Логи администратора
    path('admin-panel/admin-logs/', AdminLogListView.as_view(), name='admin_log_list'),
    path('admin-panel/admin-logs/add/', AdminLogCreateView.as_view(), name='admin_log_add'),
    path('admin-panel/admin-logs/<int:pk>/edit/', AdminLogUpdateView.as_view(), name='adminlog_edit'),
    path('admin-panel/admin-logs/<int:pk>/delete/', AdminLogDeleteView.as_view(), name='adminlog_delete'),

    # Логи модераторов
    path('admin-panel/moderator-logs/', ModeratorLogListView.as_view(), name='moderator_log_list'),
    path('admin-panel/moderator-logs/add/', ModeratorLogCreateView.as_view(), name='moderator_log_add'),
    path('admin-panel/moderator-logs/<int:pk>/edit/', ModeratorLogUpdateView.as_view(), name='moderator_log_edit'),
    path('admin-panel/moderator-logs/<int:pk>/delete/', ModeratorLogDeleteView.as_view(), name='moderator_log_delete'),

    # Назначения
    path('admin-panel/purposes/', PurposeListView.as_view(), name='purpose_list'),
    path('admin-panel/purposes/add/', PurposeCreateView.as_view(), name='purpose_add'),
    path('admin-panel/purposes/<int:pk>/edit/', PurposeUpdateView.as_view(), name='purpose_edit'),
    path('admin-panel/purposes/<int:pk>/delete/', PurposeDeleteView.as_view(), name='purpose_delete'),
    
    # UserProfile
    path('admin-panel/user-profiles/', UserProfileListView.as_view(), name='userprofile_list'),
    path('admin-panel/user-profiles/add/', UserProfileCreateView.as_view(), name='userprofile_add'),
    path('admin-panel/user-profiles/<int:pk>/edit/', UserProfileUpdateView.as_view(), name='userprofile_edit'),
    path('admin-panel/user-profiles/<int:pk>/delete/', UserProfileDeleteView.as_view(), name='userprofile_delete'),

    # Landlord
    path('admin-panel/landlords/', LandlordListView.as_view(), name='landlord_list'),
    path('admin-panel/landlords/add/', LandlordCreateView.as_view(), name='landlord_add'),
    path('admin-panel/landlords/<int:pk>/edit/', LandlordUpdateView.as_view(), name='landlord_edit'),
    path('admin-panel/landlords/<int:pk>/delete/', LandlordDeleteView.as_view(), name='landlord_delete'),

    # Moderator
    path('admin-panel/moderators/', ModeratorListView.as_view(), name='moderator_list'),
    path('admin-panel/moderators/add/', ModeratorCreateView.as_view(), name='moderator_add'),
    path('admin-panel/moderators/<int:pk>/edit/', ModeratorUpdateView.as_view(), name='moderator_edit'),
    path('admin-panel/moderators/<int:pk>/delete/', ModeratorDeleteView.as_view(), name='moderator_delete'),

    # Reviews
    path('admin-panel/reviews/', ReviewListView.as_view(), name='review_list'),
    path('admin-panel/reviews/add/', ReviewCreateView.as_view(), name='review_add'),
    path('admin-panel/reviews/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
    path('admin-panel/reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),

    path('admin-panel/users/', UserListView.as_view(), name='user_list'),
    path('admin-panel/users/<int:pk>/set_active/', UserSetActiveView.as_view(), name='user_set_active'),
    path('admin-panel/users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

