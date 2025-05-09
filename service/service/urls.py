from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
urlpatterns = [
    # если пользователь заходит на корневой URL, перенаправляем его на 'client_list'
    path('', lambda request: redirect('client_list')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="firm/login.html"), name='login'),
    path('admin/', admin.site.urls),
    path('', include('firm.urls')),
]