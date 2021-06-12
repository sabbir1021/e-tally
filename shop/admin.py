from django.contrib import admin
from .models import Shop
# Register your models here.

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['owner','name','phone','address']
    search_fields = ['owner__username','name','phone','address']
    autocomplete_fields = ['owner']
    list_per_page = 20