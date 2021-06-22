from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Shop
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    shop_name = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()
    class Meta:
        model = get_user_model()
        fields = ('email', 'username','shop_name','phone','address',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            label=_("E-mail"), max_length=75)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('shop_name', 'phone', 'address',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name',)