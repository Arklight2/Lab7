# firm/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Маршруты для работы с записями Client
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/edit/<int:pk>/', views.update_client, name='update_client'),
    path('clients/delete/<int:pk>/', views.delete_client, name='delete_client'),
    path('clients/export/excel/', views.export_clients_excel, name='export_clients_excel'),
    path('clients/export/word/', views.export_clients_word, name='export_clients_word'),
    path('clients/export/pdf/', views.export_clients_pdf, name='export_clients_pdf'),

    # Маршруты для регистрации и аутентификации
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="firm/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_recovery/', views.password_recovery, name='password_recovery'),

    # Дополнительно можно подключить стандартные маршруты сброса пароля от Django
]
