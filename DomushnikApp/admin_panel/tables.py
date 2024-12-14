import django_tables2 as tables
from DomushnikApp.models import *
from django.urls import reverse
from django.utils.html import format_html

class CustomTable(tables.Table):
    """
    Custom reusable table with default actions dropdown for models.
    """
    actions = tables.Column(empty_values=(), verbose_name="Действия", orderable=False)

    class Meta:
        template_name = "django_tables2/bootstrap4.html"

    def render_actions(self, record):
        """
        Generates the actions dropdown for the table rows.
        The `Meta.model` is used to dynamically generate the edit and delete URLs.
        """
        edit_url = reverse(f"{self.Meta.model._meta.model_name}_edit", args=[record.pk])
        delete_url = reverse(f"{self.Meta.model._meta.model_name}_delete", args=[record.pk])

        return format_html(
            '''
            <div class="dropdown">
                <button class="btn btn-secondary btn dropdown-toggle" type="button" id="dropdownMenuButton{0}" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-ellipsis-v"></i>
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton{0}">
                    <li>
                        <a class="dropdown-item" href="{1}">
                            <i class="fas fa-edit me-2"></i>Изменить
                        </a>
                    </li>
                    <li>
                        <a class="dropdown-item text-danger" href="{2}">
                            <i class="fas fa-trash me-2"></i>Удалить
                        </a>
                    </li>
                </ul>
            </div>
            ''',
            record.pk,
            edit_url,
            delete_url
        )


class AddressTable(CustomTable):
    """
    Table for displaying and managing Address objects.
    """
    class Meta(CustomTable.Meta):
        model = Address
        fields = ("city", "state", "country", "zip_code", "street", "house")


class PropertyTypeTable(CustomTable):
    """
    Table for displaying and managing PropertyType objects.
    """
    class Meta(CustomTable.Meta):
        model = PropertyType
        fields = ("name", "description")


class PropertyTable(CustomTable):
    """
    Table for displaying and managing Property objects.
    """
    class Meta(CustomTable.Meta):
        model = Property
        fields = ("landlord", "type", "address", "price_per_month", "area", "number_of_rooms", "availability_status")


class AmenityTable(CustomTable):
    """
    Table for displaying and managing Amenity objects.
    """
    class Meta(CustomTable.Meta):
        model = Amenity
        fields = ('name',)  


class RentalTable(CustomTable):
    """
    Table for displaying and managing Rental objects.
    """
    class Meta(CustomTable.Meta):
        model = Rental
        fields = ("property", "tenant", "start_date", "end_date", "is_active")


class PaymentTable(CustomTable):
    """
    Table for displaying and managing Payment objects.
    """
    class Meta(CustomTable.Meta):
        model = Payment
        fields = ("rental", "amount", "payment_date", "is_paid")


class RentalApplicationTable(CustomTable):
    """
    Table for displaying and managing RentalApplication objects.
    """
    class Meta(CustomTable.Meta):
        model = RentalApplication
        fields = ("tenant", "property", "application_date", "status", "purpose", "specific_requirements")

    
class NotificationTypeTable(CustomTable):
    """
    Table for displaying and managing NotificationType objects.
    """
    class Meta(CustomTable.Meta):
        model = NotificationType
        fields = ("name",)


class NotificationTable(CustomTable):
    """
    Table for displaying and managing Notification objects.
    """
    class Meta(CustomTable.Meta):
        model = Notification
        fields = ("notification_type", "recipient", "content", "sent_date")


class PurposeTable(CustomTable):
    """
    Table for displaying and managing Purpose objects.
    """
    class Meta(CustomTable.Meta):
        model = Purpose
        fields = ("name",)


class AdminLogTable(CustomTable):
    """
    Table for displaying and managing AdminLog objects.
    """
    class Meta(CustomTable.Meta):
        model = AdminLog
        fields = ("admin", "action", "action_date")


class ModeratorLogTable(CustomTable):
    """
    Table for displaying and managing ModeratorLog objects.
    """
    class Meta(CustomTable.Meta):
        model = ModeratorLog
        fields = ("moderator", "action", "action_date")


class ReviewTable(CustomTable):
    """
    Table for displaying and managing Review objects.
    """
    class Meta(CustomTable.Meta):
        model = Review
        fields = ("landlord", "tenant", "rating", "comment", "created_at")


class ModeratorTable(CustomTable):
    """
    Table for displaying and managing Moderator objects.
    """
    class Meta(CustomTable.Meta):
        model = Moderator
        fields = ("user__username", "user__first_name", "user__last_name")



class UserProfileTable(CustomTable):
    """
    Table for displaying and managing UserProfile objects.
    """
    class Meta(CustomTable.Meta):
        model = UserProfile
        fields = ("user__username", "first_name", "last_name", "email", "phone_number", "avatar")


class LandlordTable(CustomTable):
    """
    Table for displaying and managing Landlord objects.
    """
    class Meta(CustomTable.Meta):
        model = Landlord
        fields = ("user__username", "first_name", "last_name", "rating", "company_name", "company_logo")


class UserTable(tables.Table):
    """
    Table for displaying and managing User objects.
    """
    actions = tables.Column(empty_values=(), verbose_name="Действия", orderable=False)

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_active")

    def render_actions(self, record):
        """
        Renders the actions (Set Active/Inactive, Edit, Delete) dropdown.
        """
        activate_url = reverse('user_set_active', args=[record.pk])
        edit_url = reverse('user_edit', args=[record.pk])

        return format_html(
            '''
            <div class="dropdown">
                <button class="btn btn-secondary btn dropdown-toggle" type="button" id="dropdownMenuButton{0}" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-ellipsis-v"></i>
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton{0}">
                    <li>
                        <a class="dropdown-item" href="{1}">
                            <i class="fas fa-edit me-2"></i>Редактировать
                        </a>
                    </li>
                    <li>
                        <a class="dropdown-item" href="{2}">
                            <i class="fas fa-user-check me-2"></i>  
                            {3}
                        </a>
                    </li>
                </ul>
            </div>
            ''',
            record.pk,
            edit_url,
            activate_url,
            "Активировать" if not record.is_active else "Деактивировать"
        )
    

class BackupTable(tables.Table):
    """
    Custom table for displaying backups with actions (restore, delete).
    """
    actions = tables.Column(empty_values=(), verbose_name="Действия", orderable=False)

    class Meta:
        model = Backup
        template_name = "django_tables2/bootstrap4.html"
        fields = ("created_at", "file_path")

    def render_actions(self, record):
        """
        Generates the actions dropdown for the table rows.
        The `Meta.model` is used to dynamically generate the restore and delete URLs.
        """
        restore_url = reverse('backup_restore', args=[record.pk])
        delete_url = reverse('backup_delete', args=[record.pk])

        return format_html(
            '''
            <div class="dropdown">
                <button class="btn btn-secondary btn dropdown-toggle" type="button" id="dropdownMenuButton{0}" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-ellipsis-v"></i>
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton{0}">
                    <li>
                        <a class="dropdown-item" href="{1}">
                            <i class="fas fa-undo me-2"></i>Восстановить
                        </a>
                    </li>
                    <li>
                        <a class="dropdown-item text-danger" href="{2}">
                            <i class="fas fa-trash me-2"></i>Удалить
                        </a>
                    </li>
                </ul>
            </div>
            ''',
            record.pk,
            restore_url,
            delete_url
        )