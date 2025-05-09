# firm/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Регулярка для проверки, что имена начинаются с прописной буквы и содержат только кириллические буквы
NAME_REGEX = r'^[А-ЯЁ][а-яё]+$'
name_validator = RegexValidator(regex=NAME_REGEX,
                                message="Поле должно начинаться с прописной буквы и содержать только кириллические буквы.")


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с дополнительными полями."""
    patronymic = models.CharField("Отчество", max_length=255, validators=[name_validator])

    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
    )
    role = models.CharField("Роль", max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class OrderStatus(models.Model):
    name = models.CharField("Статус заказа", max_length=255)

    def __str__(self):
        return self.name


class PaymentStatus(models.Model):
    name = models.CharField("Статус платежа", max_length=255)

    def __str__(self):
        return self.name


class Client(models.Model):
    surname = models.CharField("Фамилия", max_length=255, validators=[name_validator])
    name = models.CharField("Имя", max_length=255, validators=[name_validator])
    email = models.EmailField("E-mail", unique=True)
    registration_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return f"{self.surname} {self.name}"


class Courier(models.Model):
    surname = models.CharField("Фамилия", max_length=255, validators=[name_validator])
    name = models.CharField("Имя", max_length=255, validators=[name_validator])
    email = models.EmailField("E-mail", unique=True)
    registration_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='couriers')

    def __str__(self):
        return f"{self.surname} {self.name}"


class Product(models.Model):
    product_name = models.CharField("Наименование продукта", max_length=255)
    price = models.DecimalField("Цена", decimal_places=2, max_digits=10)
    category = models.CharField("Категория", max_length=255, blank=True, null=True)
    stock = models.IntegerField("Количество на складе", default=0)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус заказа")
    content = models.TextField("Содержание", blank=True, null=True)
    creation_date = models.DateTimeField("Дата создания", auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Курьер")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Заказ #{self.id} клиента {self.client}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    amount = models.IntegerField("Количество")
    price = models.DecimalField("Цена", decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Элемент заказа #{self.id}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    payment_date = models.DateTimeField("Дата платежа", auto_now_add=True)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.SET_NULL, null=True,
                                       verbose_name="Статус платежа")
    amount = models.DecimalField("Сумма", decimal_places=2, max_digits=10)

    def __str__(self):
        return f"Платеж #{self.id} от клиента {self.client}"


class Feedback(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    review_date = models.DateTimeField("Дата отзыва", auto_now_add=True)
    comment = models.TextField("Комментарий", blank=True, null=True)
    rating = models.IntegerField("Рейтинг", validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Отзыв #{self.id} от клиента {self.client}"


class Category(models.Model):
    category_name = models.CharField("Категория", max_length=255, unique=True)

    def __str__(self):
        return self.category_name
