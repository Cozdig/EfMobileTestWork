from django.db import models

# Create your models here.

class CustomUser(models.Model):
    first_name = models.CharField(max_length=30, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=50, blank=False, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=40, blank=False, verbose_name="Отчество")
    email = models.EmailField(unique=True, blank=False, verbose_name="Электронная почта")
    first_password = models.CharField(max_length=50, blank=False, verbose_name="Пароль")
    second_password = models.CharField(max_length=50, blank=False, verbose_name="Подтверждение пароля")
    is_active = models.BooleanField(verbose_name="Активный аккаунт")