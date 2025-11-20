from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.
    Логин по email, добавлены аватар, телефон, страна.
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Страна'
    )

    USERNAME_FIELD = 'email'          # используем email как логин
    REQUIRED_FIELDS = ['username']    # что дополнительно спрашивать при createsuperuser

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
