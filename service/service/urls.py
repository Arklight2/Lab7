# service/urls.py
from django.contrib import admin
from django.urls import path, include
from firm import views # Импортируйте views из вашего приложения firm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), # Добавьте или раскомментируйте эту строку для главной страницы
    path('firm/', include('firm.urls', namespace='firm')), # Включаем urls.py из firm с пространством имен 'firm'
    # ... другие URL-адреса
]