from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Shop
User = get_user_model()

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2',)
        }),
    )
    model = User
    list_display = ['email', 'username', 'first_name',
                    'last_name', 'is_staff','active']
    list_filter = ['is_staff']
    list_editable = ['active','is_staff']
    list_perpage = 20


admin.site.register(User, CustomUserAdmin)
admin.site.register(Shop)
