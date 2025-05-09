
from django.urls import path
from . import views
from .views import ClientListView, CustomLoginView, CustomLogoutView # Импортируйте ваши представления

app_name = 'firm' # Определение пространства имен для URL-адресов

urlpatterns = [
    # URL для главной страницы (если вы определяете ее в firm/urls.py)
    # path('', views.index, name='index'),

    # URL для списка клиентов (используйте вашу Function-Based View или Class-Based View)
    # path('clients/', views.client_list, name='client_list'), # Для Function-Based View
    path('clients/', ClientListView.as_view(), name='client_list'), # Для Class-Based View (рекомендуется для списков)

    # URL для создания клиента
    path('clients/create/', views.client_create, name='client_create'),

    # URL для детального просмотра клиента (с передачей id клиента в URL)
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),

    # URL для обновления клиента (с передачей id клиента в URL)
    path('clients/<int:pk>/update/', views.client_update, name='client_update'),

    # URL для удаления клиента (с передачей id клиента в URL)
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),


    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'), # Убедитесь, что используете CustomLoginView.as_view()
    path('logout/', CustomLogoutView.as_view(), name='logout'), # Убедитесь, что используете CustomLogoutView.as_view()


    # URL-адреса для сброса пароля
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]



