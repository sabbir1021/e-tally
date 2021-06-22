from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
User= get_user_model
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'



class Shop(models.Model):
    user = models.OneToOneField(User,related_name='user_shop', on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = '1. Shop'

    def __str__(self):
        return self.shop_name

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Shop.objects.create(user=instance)
        else:
            instance.user_shop.save()
    except Exception as e:
        pass