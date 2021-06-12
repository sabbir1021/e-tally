from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    address = models.CharField(max_length=250)


    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = '1. Shop'

    def __str__(self):
        return self.name
    
