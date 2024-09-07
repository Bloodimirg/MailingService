from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=40, **NULLABLE, verbose_name="Телефон (Не обязательно)")
    avatar = models.ImageField(upload_to='users/avatars', **NULLABLE, verbose_name='Аватар (Не обязательно)')
    country = models.CharField(max_length=50, **NULLABLE, verbose_name='Страна (Не обязательно)')

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE, help_text='Не обязательно')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["email",]
        permissions = [
                       ('can_view_users', 'Can view users'),
                       ('can_block_users', 'Can block users'),
                       ]

    def __str__(self):
        return self.email