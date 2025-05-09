from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, OrderStatus, PaymentStatus, Client, Courier, Product, Order, OrderItem, Payment, Feedback, Category

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('patronymic', 'role')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronymic')
    ordering = ('username',)


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'email', 'registration_date', 'created_by')
    list_filter = ('registration_date', 'created_by')
    search_fields = ('surname', 'name', 'email')
    date_hierarchy = 'registration_date'


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'email', 'registration_date', 'created_by')
    list_filter = ('registration_date', 'created_by')
    search_fields = ('surname', 'name', 'email')
    date_hierarchy = 'registration_date'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category', 'stock')
    list_filter = ('category', 'stock')
    search_fields = ('product_name', 'category')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_status', 'client', 'courier', 'creation_date', 'created_by')
    list_filter = ('order_status', 'creation_date', 'client', 'courier', 'created_by')
    search_fields = ('content',)
    date_hierarchy = 'creation_date'
    raw_id_fields = ('client', 'courier', 'order_status') # Удобно для выбора связанных объектов


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'amount', 'price')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__product_name')
    raw_id_fields = ('order', 'product')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'client', 'payment_date', 'payment_status', 'amount', 'created_by')
    list_filter = ('payment_date', 'payment_status', 'client', 'order', 'created_by')
    search_fields = ('order__id', 'client__surname', 'client__name')
    date_hierarchy = 'payment_date'
    raw_id_fields = ('order', 'client', 'payment_status')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'client', 'review_date', 'rating', 'created_by')
    list_filter = ('review_date', 'rating', 'client', 'order', 'created_by')
    search_fields = ('comment', 'client__surname', 'client__name')
    date_hierarchy = 'review_date'
    raw_id_fields = ('order', 'client')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)
