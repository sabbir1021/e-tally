from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import datetime
User = get_user_model()
from django.db.models import Max, Min , Count , Sum
# Create your models here.

    
class Customer(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

    @property
    def cost_amount(self):
        customer_cost = self.cost_pay.filter(cost=True).aggregate(Sum('amount'))['amount__sum']
        customer_pay = self.cost_pay.filter(pay=True).aggregate(Sum('amount'))['amount__sum']
        if customer_cost!=None and customer_pay!=None:
            final = customer_cost - customer_pay
        else:
            final = 0
        return final

    def __str__(self):
        return self.name

class Customer_Cost_Pay(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', related_name='cost_pay', on_delete=models.CASCADE)
    amount = models.IntegerField()
    describe = models.CharField(max_length=200)
    cost = models.BooleanField()
    pay = models.BooleanField()
    date = models.DateTimeField(default=datetime.now(),auto_now=False, auto_now_add=False)
    def __str__(self):
        return str(self.customer)
    

class Supplier(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
           
    def __str__(self):
        return self.name

class Supplier_Buy_Pay(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier', related_name='supplier_cost', on_delete=models.CASCADE)
    amount = models.IntegerField()
    describe = models.CharField(max_length=200)
    buy = models.BooleanField()
    pay = models.BooleanField()
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.supplier)


class Cash(models.Model):
    user = models.ForeignKey(User, related_name="cash", on_delete=models.CASCADE)
    amount = models.IntegerField()
    describe = models.CharField(max_length=200)
    sell_cash = models.BooleanField()
    buy = models.BooleanField()
    cost = models.BooleanField()
    date = models.DateTimeField(default=datetime.now(),auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.amount)

