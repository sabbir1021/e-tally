from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'
