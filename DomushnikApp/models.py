from django.db import models
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.db.models import Model
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

# Выборы для различных полей
ENERGY_TYPE_CHOICES = [
    ('A++', 'A++'),
    ('A+', 'A+'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
]

HEATING_TYPE_CHOICES = [
    ('Газовый', 'Газовый'),
    ('Водяной', 'Водяной'),
    ('Электрический', 'Электрический')
]


AVAILABILITY_STATUS_CHOICES = [
    ('available', 'Доступно'),
    ('rented', 'Арендовано'),
    ('under_maintenance', 'На ремонте'),
]

PROPERTY_CONDITION_CHOICES = [
    ('new', 'Новое'),
    ('good', 'Хорошее'),
    ('needs_renovation', 'Требует ремонта'),
]

PROPERTY_USAGE_CHOICES = [
    ('residential', 'Жилое'),
    ('commercial', 'Коммерческое'),
    ('industrial', 'Индустриальное'),
]

APPLICATION_STATUS_CHOICES = [
    ('pending', 'В ожидании'),
    ('approved', 'Одобрено'),
    ('rejected', 'Отклонено'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Пользователь")
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    bio = models.TextField(null=True, blank=True, verbose_name="О себе")

    def __str__(self):
        return self.user.username

class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord_profile', verbose_name="Пользователь")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Рейтинг")
    is_legal_entity = models.BooleanField(default=False, verbose_name="Юридическое лицо")
    company_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название компании")
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True, verbose_name="Лого компании")

    def __str__(self):
        return f"Арендодатель: {self.user.first_name} {self.user.last_name}"


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moderator_profile', verbose_name="Пользователь")

    def __str__(self):
        return f"Модератор: {self.user.first_name} {self.user.last_name}"


class Review(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='reviews', verbose_name="Арендодатель")
    tenant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews', verbose_name="Арендатор")
    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Рейтинг")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.tenant.first_name} {self.tenant.last_name} для {self.landlord.user.first_name} {self.landlord.user.last_name}"


class Purpose(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Назначение"
        verbose_name_plural = "Назначения"

    def __str__(self):
        return self.name

class Address(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Долгота")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город")
    street = models.CharField(max_length=100, null=True, blank=True, verbose_name="Улица")
    state = models.CharField(max_length=100, null=True, blank=True, verbose_name="Область")
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name="Страна")
    zip_code = models.CharField(max_length=10, null=True, blank=True, verbose_name="Индекс")
    house = models.CharField(max_length=50, null=True, blank=True, verbose_name="Дом")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return f"{self.house}, {self.street}, {self.state}, {self.city}, {self.country}"

class PropertyType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Тип недвижимости"
        verbose_name_plural = "Типы недвижимости"

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100, verbose_name="Удобство")

    class Meta:
        verbose_name = "Удобство"
        verbose_name_plural = "Удобства"

    def __str__(self):
        return self.name

class Property(models.Model):
    property_name = models.CharField(max_length=255, verbose_name="Название недвижимости")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', verbose_name="Арендодатель")
    type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='properties', verbose_name="Тип")
    address = models.ForeignKey(Address,null=True, on_delete=models.CASCADE, verbose_name="Адрес")
    price_per_month = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Цена за месяц")
    area = models.FloatField(null=True, blank=True, verbose_name="Площадь")
    number_of_rooms = models.IntegerField(null=True, blank=True, verbose_name="Количество комнат")
    furnished = models.BooleanField(default=False, verbose_name="Мебель")
    floor = models.IntegerField(null=True, blank=True, verbose_name="Этаж")
    total_floors = models.IntegerField(null=True, blank=True, verbose_name="Всего этажей")
    year_built = models.IntegerField(null=True, blank=True, verbose_name="Год постройки")
    heating_type = models.CharField(max_length=50, choices=HEATING_TYPE_CHOICES, null=True, blank=True, verbose_name="Тип отопления")
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_STATUS_CHOICES,
        default='available',
        verbose_name="Статус доступности"
    )
    parking = models.BooleanField(default=False, verbose_name="Парковка")
    balcony = models.BooleanField(default=False, verbose_name="Балкон")
    pets_allowed = models.BooleanField(default=False, verbose_name="Можно с животными")
    internet_access = models.BooleanField(default=False, verbose_name="Доступ в интернет")
    property_condition = models.CharField(
        max_length=20,
        choices=PROPERTY_CONDITION_CHOICES,
        null=True,
        blank=True,
        verbose_name="Состояние недвижимости"
    )
    property_usage = models.CharField(
        max_length=20,
        choices=PROPERTY_USAGE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Назначение недвижимости"
    )
    energy_efficiency_class = models.CharField(max_length=10, choices=ENERGY_TYPE_CHOICES, null=True, blank=True, verbose_name="Класс энергопотребления")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    amenities = models.ManyToManyField(Amenity, related_name='properties', blank=True, verbose_name="Удобства")

    class Meta:
        verbose_name = "Недвижимость"
        verbose_name_plural = "Недвижимость"

    def __str__(self):
        return f"Недвижимость {self.address} от {self.landlord.username}"

class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos', verbose_name="Недвижимость")
    photo = models.ImageField(upload_to='property_photos/', verbose_name="Фото")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Фото недвижимости"
        verbose_name_plural = "Фотографии недвижимости"

    def __str__(self):
        return f"Фото {self.id} недвижимости {self.property.id}"

class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features', verbose_name="Недвижимость")
    feature_name = models.CharField(max_length=100, verbose_name="Название характеристики")
    feature_value = models.CharField(max_length=255, verbose_name="Значение характеристики")

    class Meta:
        verbose_name = "Характеристика недвижимости"
        verbose_name_plural = "Характеристики недвижимости"

    def __str__(self):
        return f"{self.feature_name}: {self.feature_value}"

class Rental(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rentals', verbose_name="Недвижимость")
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals', verbose_name="Арендатор")
    start_date = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренда"

    def __str__(self):
        return f"Аренда {self.id} недвижимости {self.property.id}"

class RentalApplication(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name="Арендатор")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='applications', verbose_name="Недвижимость")
    application_date = models.DateField(auto_now_add=True, verbose_name="Дата подачи заявки")
    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заявки"
    )
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, verbose_name="Назначение")
    specific_requirements = models.TextField(null=True, blank=True, verbose_name="Особые требования")

    class Meta:
        verbose_name = "Заявка на аренду"
        verbose_name_plural = "Заявки на аренду"

    def __str__(self):
        return f"Заявка {self.id} от {self.tenant.username}"

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='payments', verbose_name="Аренда")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    payment_date = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж {self.id} за аренду {self.rental.id}"

class NotificationType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название типа уведомления")

    class Meta:
        verbose_name = "Тип уведомления"
        verbose_name_plural = "Типы уведомлений"

    def __str__(self):
        return self.name

class Notification(models.Model):
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE, verbose_name="Тип уведомления")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Получатель")
    content = models.TextField(verbose_name="Содержание")
    sent_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"Уведомление {self.id} для {self.recipient.username}"

class Backup(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    file_path = models.CharField(max_length=255, verbose_name="Название файла")

    class Meta:
        verbose_name = "Резервная копия"
        verbose_name_plural = "Резервные копии"

    def __str__(self):
        return f"Резервная копия {self.id} от {self.created_at}"

class AdminLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_logs', verbose_name="Администратор")
    action = models.TextField(verbose_name="Действие")
    action_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата действия")

    class Meta:
        verbose_name = "Лог администратора"
        verbose_name_plural = "Логи администратора"

    def __str__(self):
        return f"Лог {self.id} от администратора {self.admin.username}"

class ModeratorLog(models.Model):
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderator_logs', verbose_name="Модератор")
    action = models.TextField(verbose_name="Действие")
    action_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата действия")

    class Meta:
        verbose_name = "Лог модератора"
        verbose_name_plural = "Логи модераторов"

    def __str__(self):
        return f"Лог {self.id} от модератора {self.moderator.username}"

# Функция для записи логов
def log_admin_action(action, model_name, instance, user, changes=None):
    if changes:
        change_details = f"Изменения: {changes}"
    else:
        change_details = "Без изменений."
    AdminLog.objects.create(
        admin=user,
        action=f"{action} в {model_name}: {instance}. {change_details}"
    )


# Отслеживание изменений перед сохранением
@receiver(pre_save)
def log_model_changes(sender, instance, **kwargs):
    if not issubclass(sender, models.Model) or sender == AdminLog or sender == ModeratorLog:
        return  # Исключаем системные таблицы логов

    user = getattr(instance, '_updated_by', None)
    if user and user.is_authenticated:
        model_name = sender._meta.verbose_name
        # Попробуем найти текущую запись для сравнения
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_data = model_to_dict(old_instance)
        except sender.DoesNotExist:
            old_data = None

        new_data = model_to_dict(instance)

        # Сравнение данных
        changes = {}
        if old_data:
            for field, old_value in old_data.items():
                new_value = new_data.get(field)
                if old_value != new_value:
                    changes[field] = {"from": old_value, "to": new_value}

        action = "Обновление" if old_data else "Создание"
        log_admin_action(action, model_name, instance, user, changes)


# Сигнал для обновления рейтинга после сохранения отзыва
@receiver(post_save, sender=Review)
def update_landlord_rating(sender, instance, created, **kwargs):
    if created:
        calculate_landlord_rating(instance.landlord)


# Функция для подсчета рейтинга арендодателя
def calculate_landlord_rating(landlord):
    reviews = landlord.reviews.all()
    if reviews:
        total_rating = sum(review.rating for review in reviews)
        new_rating = total_rating / len(reviews)
        landlord.rating = round(new_rating, 2)
        landlord.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


