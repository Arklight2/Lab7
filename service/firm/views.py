from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm, ClientCreateForm, ClientUpdateForm, ClientViewForm
from .models import CustomUser, Client, Order, Product, OrderStatus, PaymentStatus, Courier, OrderItem, Payment, Feedback, Category # Импортируем все модели
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import login # Импортируем функцию login (если нужно автоматический вход после регистрации)


# Представление для главной страницы
def index(request):
    latest_clients = Client.objects.order_by('-registration_date')[:5]
    latest_orders = Order.objects.order_by('-creation_date')[:5]
    latest_products = Product.objects.order_by('-id')[:5]

    context = {
        'latest_clients': latest_clients,
        'latest_orders': latest_orders,
        'latest_products': latest_products,
    }
    return render(request, 'firm/index.html', context)

# Представление для регистрации
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Опционально: автоматический вход после регистрации
            # login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
            return redirect('firm:login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()
    # ИСПРАВЛЕНО: Рендерим шаблон регистрации
    return render(request, 'firm/register.html', {'form': form})


# Представление для входа (используем стандартную LoginView с кастомным шаблоном и формой)
class CustomLoginView(LoginView):
    # ИСПРАВЛЕНО: Указываем шаблон входа
    template_name = 'firm/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True # Перенаправлять авторизованных пользователей

    # success_url = '/firm/clients/' # Можно указать здесь или использовать LOGIN_REDIRECT_URL в settings.py

    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {self.request.user.username}!')
        # super().form_valid(form) выполнит перенаправление на success_url или LOGIN_REDIRECT_URL
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return super().form_invalid(form)


# Представление для выхода (используем стандартную LogoutView)
class CustomLogoutView(LogoutView):
    next_page = '/' # Перенаправлять на главную после выхода


# Представления для сброса пароля (используем стандартные классы с кастомными шаблонами и формами)
class CustomPasswordResetView(PasswordResetView):
    template_name = 'firm/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'firm/password_reset_email.html'
    subject_template_name = 'firm/password_reset_subject.txt'
    success_url = '/firm/password_reset/done/'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'firm/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'firm/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = '/firm/reset/done/'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'firm/password_reset_complete.html'


# Представление для просмотра списка клиентов (Class-Based View)
# @login_required # Если страница требует входа, используйте декоратор
class ClientListView(ListView):
    model = Client
    template_name = 'firm/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        # Логика фильтрации по правам доступа
        if self.request.user.is_authenticated: # Проверка аутентификации
            if self.request.user.is_staff: # Проверка на админа (предполагая, что is_staff означает админа)
                return Client.objects.all()
            else:
                # Обычный пользователь видит только своих клиентов (по created_by)
                return Client.objects.filter(created_by=self.request.user)
        else:
            # Если пользователь не аутентифицирован, возвращаем пустой queryset или что-то другое
            # Если страница защищена @login_required, эта ветка не будет достигнута.
            return Client.objects.none() # Возвращаем пустой список для неаутентифицированных

# Представление для создания клиента
@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, 'Клиент успешно создан!')
            return redirect('firm:client_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ClientCreateForm()
    return render(request, 'firm/client_create.html', {'form': form})


# Представление для детального просмотра клиента
@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    # Проверка прав доступа
    if not request.user.is_staff and client.created_by != request.user:
        messages.error(request, 'У вас нет прав для просмотра этого клиента.')
        return redirect('firm:client_list')

    form = ClientViewForm(instance=client)
    return render(request, 'firm/client_detail.html', {'client': client, 'form': form})


# Представление для обновления клиента
@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    # Проверка прав доступа
    if not request.user.is_staff and client.created_by != request.user:
        messages.error(request, 'У вас нет прав для редактирования этого клиента.')
        return redirect('firm:client_list')

    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные клиента успешно обновлены!')
            return redirect('firm:client_detail', pk=client.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ClientUpdateForm(instance=client)
    return render(request, 'firm/client_update.html', {'form': form, 'client': client})


# Представление для удаления клиента
@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    # Проверка прав доступа
    if not request.user.is_staff and client.created_by != request.user:
        messages.error(request, 'У вас нет прав для удаления этого клиента.')
        return redirect('firm:client_list')

    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Клиент успешно удален!')
        return redirect('firm:client_list')

    return render(request, 'firm/client_confirm_delete.html', {'client': client})

# --- Представления для других моделей (примеры - нужно реализовать полный CRUD для всех) ---

# Пример: Представление для просмотра списка продуктов
# @login_required # Если страница требует входа
# class ProductListView(ListView):
#     model = Product
#     template_name = 'firm/product_list.html' # Убедитесь, что этот шаблон существует
#     context_object_name = 'products'

#     def get_queryset(self):
#         # Здесь может быть логика фильтрации по правам доступа, если необходимо
#         return Product.objects.all()


# Пример: Представление для создания продукта
# @login_required
# def product_create(request):
#     # Нужна форма для продукта (ProductForm в forms.py)
#     # Нужен шаблон для создания продукта (firm/templates/firm/product_create.html)
#     # Логика обработки формы
#     pass # Заглушка - нужно реализовать


# ... и так далее для всех остальных моделей (OrderStatus, PaymentStatus, Courier, Order, OrderItem, Payment, Feedback, Category)