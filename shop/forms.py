from django import forms
from django.contrib.auth.models import User

from .models import Customer , Customer_Cost_Pay , Cash ,Supplier, Supplier_Buy_Pay

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'phone', 'address')

class CustomerCostPayForm(forms.ModelForm):
    class Meta:
        model = Customer_Cost_Pay
        fields = ('amount', 'describe', 'cost' ,'pay')

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('name', 'phone', 'address')

class SupplierBuyPayForm(forms.ModelForm):
    class Meta:
        model = Supplier_Buy_Pay
        fields = ('amount', 'describe', 'buy' ,'pay')

class CashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = ('amount', 'describe','sell_cash','buy','cost')