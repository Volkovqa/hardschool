from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    "null": True,
    "blank": True
}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Почта", unique=True)

    phone_number = models.CharField(max_length=35, verbose_name="Номер телефона", **NULLABLE)
    location = models.CharField(max_length=150, verbose_name="Город", **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

