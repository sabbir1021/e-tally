from django.contrib import admin
from .models import  Customer , Cash , Customer_Cost_Pay , Supplier , Supplier_Buy_Pay
# Register your models here.


@admin.register(Cash)
class CashAdmin(admin.ModelAdmin):
    list_display = ['amount','describe','sell_cash','buy','cost','date']
    search_fields = []
    autocomplete_fields = []
    list_per_page = 20


admin.site.register(Customer)
admin.site.register(Customer_Cost_Pay)
admin.site.register(Supplier)
admin.site.register(Supplier_Buy_Pay)
