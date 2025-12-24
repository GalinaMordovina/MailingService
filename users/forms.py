from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomUser


class SignUpForm(UserCreationForm):
    """Форма регистрации нового пользователя с русскими подписями."""

    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Минимум 8 символов. Не должен быть слишком простым.",
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Введите тот же пароль ещё раз.",
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone', 'country', 'avatar')

        labels = {
            'email': 'Email',
            'username': 'Логин',
            'phone': 'Телефон',
            'country': 'Страна',
            'avatar': 'Аватар',
        }

        help_texts = {
            'email': 'Введите действительный адрес электронной почты.',
            'username': 'Ваш логин (буквы, цифры и символы @ . + - _).',
            'phone': 'Необязательно.',
            'country': 'Укажите страну проживания (необязательно).',
            'avatar': 'Можно загрузить изображение профиля (необязательно).',
        }

        error_messages = {
            'email': {
                'unique': "Пользователь с таким email уже существует.",
            }
        }


class LoginForm(AuthenticationForm):
    """Форма входа с русскими подписями."""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )


class ProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone', 'country', 'avatar')

        labels = {
            'email': 'Email',
            'username': 'Логин',
            'phone': 'Телефон',
            'country': 'Страна',
            'avatar': 'Аватар',
        }
