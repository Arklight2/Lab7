# firm/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OrderStatus, PaymentStatus, Client, Courier, Product, Order, OrderItem, Payment, Feedback, Category

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'patronymic', 'role', 'email')
    list_filter = ('role',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OrderStatus)
admin.site.register(PaymentStatus)
admin.site.register(Client)
admin.site.register(Courier)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(Category)
