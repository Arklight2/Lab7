# firm/forms.py
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Client

# Регулярные выражения
NAME_REGEX = r'^[А-ЯЁ][а-яё]+$'
EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,5}$'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={
            'pattern': PASSWORD_REGEX,
            'title': "Пароль должен быть не менее 8 символов, содержать прописные и строчные латинские буквы, цифры и специальные символы."
        }
    ))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'first_name', 'patronymic', 'email']

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
            raise forms.ValidationError("E-mail должен быть вида логин@домен.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        if not re.match(PASSWORD_REGEX, password1):
            raise forms.ValidationError("Пароль не соответствует требованиям.")
        return password2


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['surname', 'name', 'email']
        widgets = {
            'surname': forms.TextInput(attrs={
                'pattern': NAME_REGEX,
                'title': "Фамилия должна начинаться с прописной буквы и содержать только кириллические буквы",
                'required': 'required'
            }),
            'name': forms.TextInput(attrs={
                'pattern': NAME_REGEX,
                'title': "Имя должно начинаться с прописной буквы и содержать только кириллические буквы",
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'pattern': EMAIL_REGEX,
                'title': "Введите корректный e-mail (латинские буквы, @ и домен второго-пятого уровня)",
                'required': 'required'
            }),
        }

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
