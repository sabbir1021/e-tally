from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    
    path('', views.HomeView.as_view() , name='home'),
    path('customer_form', views.CustomerFormView.as_view() , name="customer_form"),
    path('customer/<int:id>', views.CustomerView.as_view() , name='customer'),
    path('customer/details/<int:id>', views.CustomerDetailsView.as_view() , name='customer_details'),
    path('supplier_form', views.SupplierFormView.as_view() , name="supplier_form"),
    path('supplier/<int:id>', views.SupplierView.as_view() , name='supplier'),
    path('supplier/details/<int:id>', views.SupplierDetailsView.as_view() , name='supplier_details'),
    path('monthlycost' , views.MonthlyCostView.as_view(), name="monthlycost"),
    path('monthlybaki' , views.MonthlyBakiView.as_view(), name="monthlybaki"),
    path('monthlycash' , views.MonthlyCashView.as_view(), name="monthlycash"),
    path('monthlybuysell' , views.MonthlyBuySellView.as_view(), name="monthlybuysell"),

]
