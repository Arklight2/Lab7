# firm/forms.py
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser, Client

# Регулярные выражения
NAME_REGEX = r'^[А-ЯЁ][а-яё]+$'
# Улучшенная регулярка для email (поддержка доменов до 5 уровней, только латиница)
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,5}(\.[a-zA-Z]{2,3}){0,4}$' # Немного скорректировал для 5 уровней
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'


class RegistrationForm(UserCreationForm):
    patronymic = forms.CharField(label="Отчество", max_length=255)
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name', 'patronymic', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(NAME_REGEX, first_name):
            raise forms.ValidationError(
                "Имя должно начинаться с прописной буквы и содержать только кириллические буквы.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(NAME_REGEX, last_name):
            raise forms.ValidationError(
                "Фамилия должна начинаться с прописной буквы и содержать только кириллические буквы.")
        return last_name

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if not re.match(NAME_REGEX, patronymic):
            raise forms.ValidationError(
                "Отчество должно начинаться с прописной буквы и содержать только кириллические буквы.")
        return patronymic

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Введите корректный email адрес (латинские буквы, @ и домен до 5 уровней).")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        if not re.match(PASSWORD_REGEX, password1):
            raise forms.ValidationError("Пароль должен быть не менее 8 символов, содержать прописные и строчные латинские буквы, цифры и специальные символы.")
        return password2


# Форма для входа (можно использовать стандартную)
class LoginForm(AuthenticationForm):
    pass

# Форма для сброса пароля (используем стандартную)
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.TextInput(attrs={'autocomplete': 'email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
             raise forms.ValidationError("Пользователь с таким email не найден.")
        return email

# Форма для установки нового пароля после сброса (используем стандартную)
class CustomSetPasswordForm(SetPasswordForm):
    pass


class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'email']

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if not re.match(NAME_REGEX, surname):
            raise forms.ValidationError(
                "Фамилия должна начинаться с прописной буквы и содержать только кириллические буквы.")
        return surname

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(NAME_REGEX, name):
            raise forms.ValidationError(
                "Имя должно начинаться с прописной буквы и содержать только кириллические буквы.")
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Введите корректный email адрес (латинские буквы, @ и домен до 5 уровней).")
        if Client.objects.filter(email=email).exists():
             raise forms.ValidationError("Клиент с таким email уже существует.")
        return email


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'email']

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if not re.match(NAME_REGEX, surname):
            raise forms.ValidationError(
                "Фамилия должна начинаться с прописной буквы и содержать только кириллические буквы.")
        return surname

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(NAME_REGEX, name):
            raise forms.ValidationError(
                "Имя должно начинаться с прописной буквы и содержать только кириллические буквы.")
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError("Введите корректный email адрес (латинские буквы, @ и домен до 5 уровней).")
        if Client.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
             raise forms.ValidationError("Клиент с таким email уже существует.")
        return email


class ClientViewForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'email'] # Удалено 'registration_date'
        widgets = {
            'surname': forms.TextInput(attrs={'readonly': 'readonly'}),
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'registration_date': forms.DateTimeInput(attrs={'readonly': 'readonly'}), # Можно оставить виджет, он не вызывает ошибку
        }