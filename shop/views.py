from django.shortcuts import render , get_object_or_404 , redirect
from django.db.models import Max, Min , Count , Sum
from .models import Cash , Customer , Customer_Cost_Pay , Supplier , Supplier_Buy_Pay
from .forms import CashForm , CustomerForm , CustomerCostPayForm,SupplierForm, SupplierBuyPayForm
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from datetime import date 
import datetime
import time


@method_decorator(login_required, name='dispatch')
class HomeView(generic.View):
    def get(self, request, *args, **kwrags):
        form = CashForm()
        
        today_sell_cash = Cash.objects.all().filter(sell_cash=True,user=request.user,date__day = date.today().day ).aggregate(Sum('amount'))['amount__sum'] or 0
        today_sell_baki = Customer_Cost_Pay.objects.all().filter(user=request.user,cost=True,date__day = date.today().day ).aggregate(Sum('amount'))['amount__sum'] or 0
        today_sell = today_sell_cash + today_sell_baki
        
        today_sell_cash_pay = Cash.objects.all().filter(sell_cash=True,user=request.user,date__day = date.today().day).aggregate(Sum('amount'))['amount__sum'] or 0
        today_baki_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True,date__day = date.today().day).aggregate(Sum('amount'))['amount__sum'] or 0
        today_cash_buy = Cash.objects.all().filter(buy=True,user=request.user,date__day = date.today().day).aggregate(Sum('amount'))['amount__sum'] or 0
        today_cash_cost = Cash.objects.all().filter(cost=True,user=request.user,date__day = date.today().day).aggregate(Sum('amount'))['amount__sum'] or 0
        supplier_baki_pay = Supplier_Buy_Pay.objects.all().filter(user=request.user,pay=True).aggregate(Sum('amount'))['amount__sum'] or 0    
        today_cash_pay = today_sell_cash_pay + today_baki_pay - today_cash_buy - today_cash_cost - supplier_baki_pay
        
        customer_baki = Customer_Cost_Pay.objects.all().filter(user=request.user,cost=True).aggregate(Sum('amount'))['amount__sum'] or 0
        customer_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_baki = customer_baki - customer_pay

        supplier_buy = Supplier_Buy_Pay.objects.all().filter(user=request.user,buy=True).aggregate(Sum('amount'))['amount__sum'] or 0
        supplier_pay = Supplier_Buy_Pay.objects.all().filter(user=request.user,pay=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_pabe = supplier_buy - supplier_pay
        
        customers = Customer.objects.prefetch_related('cost_pay').filter(user=request.user)
        suppliers = Supplier.objects.all().filter(user=request.user)
        
        contex = {
            'form':form,
            'today_sell':today_sell,
            'today_cash_pay': today_cash_pay,
            'total_baki' : total_baki,
            'customers' : customers,
            'suppliers' : suppliers,
            'total_pabe': total_pabe
            
        }
        return render(request, 'home.html', contex)

    def post(self, request, *args, **kwargs):
        form = CashForm(request.POST)
        if form.is_valid():
            cash = form.save(commit=False)
            cash.user = request.user
            
            cash.save()
            return redirect('shop:home')
        else:
            context = {
                'form': form,
            }
            return render(request, 'home.html', context)


class CustomerView(generic.View):
    def get(self, request, *args, **kwrags):
        form = CustomerCostPayForm()
        customer = get_object_or_404(Customer, id=kwrags.get('id'))
        customer_cost = Customer_Cost_Pay.objects.filter(customer__id=kwrags.get('id'),cost=True).aggregate(Sum('amount'))['amount__sum'] or 0
        customer_pay = Customer_Cost_Pay.objects.filter(customer__id=kwrags.get('id'),pay=True).aggregate(Sum('amount'))['amount__sum'] or 0
        
        customer_baki = customer_cost - customer_pay
        contex = {
            'form' : form,
            'customer': customer,
            'customer_cost' : customer_cost,
            'customer_pay' : customer_pay ,
            'customer_baki' : customer_baki,
        }
        return render(request , "customer.html", contex)

    def post(self, request, *args, **kwrags):
        form = CustomerCostPayForm(request.POST)
        if form.is_valid():
            customer = get_object_or_404(Customer, id=kwrags.get('id'))
            cash = form.save(commit=False)
            cash.user = request.user
            cash.customer = customer
            cash.save()
            return redirect('shop:customer', id=kwrags.get('id'))
        else:
            contex = {
                'form': form,
            }
            return render(request , "customer.html", contex)


class SupplierView(generic.View):
    def get(self, request, *args, **kwrags):
        form = SupplierBuyPayForm()
        supplier = get_object_or_404(Supplier, id=kwrags.get('id'))
        supplier_buy = Supplier_Buy_Pay.objects.filter(supplier__id=kwrags.get('id'),buy=True).aggregate(Sum('amount'))['amount__sum'] or 0
        supplier_pay = Supplier_Buy_Pay.objects.filter(supplier__id=kwrags.get('id'),pay=True).aggregate(Sum('amount'))['amount__sum'] or 0
       
        supplier_baki = supplier_buy - supplier_pay
        contex = {
            'form' : form,
            'supplier': supplier,
            'supplier_buy' : supplier_buy,
            'supplier_pay' : supplier_pay ,
            'supplier_baki' : supplier_baki,
        }
        return render(request , "supplier.html", contex)

    def post(self, request, *args, **kwrags):
        form = SupplierBuyPayForm(request.POST)
        if form.is_valid():
            supplier = get_object_or_404(Supplier, id=kwrags.get('id'))
            cash = form.save(commit=False)
            cash.user = request.user
            cash.supplier = supplier
            cash.save()
            return redirect('shop:supplier', id=kwrags.get('id'))
        else:
            contex = {
                'form': form,
            }
            return render(request , "supplier.html", contex)

class CustomerDetailsView(generic.View):
    def get(self, request, *args, **kwrags):
        customer = get_object_or_404(Customer, id=kwrags.get('id'))
        customer_costs = Customer_Cost_Pay.objects.all().filter(customer__id=kwrags.get('id'),cost=True)
        customer_pays = Customer_Cost_Pay.objects.all().filter(customer__id=kwrags.get('id'),pay=True)
        customer_cost = Customer_Cost_Pay.objects.filter(customer__id=kwrags.get('id'),cost=True).aggregate(Sum('amount'))['amount__sum'] or 0
        customer_pay = Customer_Cost_Pay.objects.filter(customer__id=kwrags.get('id'),pay=True).aggregate(Sum('amount'))['amount__sum'] or 0
        
        customer_baki = customer_cost - customer_pay
        contex = {
            'customer': customer,
            'customer_costs' : customer_costs,
            'customer_pays' : customer_pays,
            'customer_cost' : customer_cost,
            'customer_pay' : customer_pay ,
            'customer_baki' : customer_baki,
        }
        return render(request, "customer_details.html",contex)

class SupplierDetailsView(generic.View):
    def get(self, request, *args, **kwrags):
        supplier = get_object_or_404(Supplier, id=kwrags.get('id'))
        supplier_buys = Supplier_Buy_Pay.objects.all().filter(supplier__id=kwrags.get('id'),buy=True)
        supplier_pays = Supplier_Buy_Pay.objects.all().filter(supplier__id=kwrags.get('id'),pay=True)
        supplier_buy = Supplier_Buy_Pay.objects.filter(supplier__id=kwrags.get('id'),buy=True).aggregate(Sum('amount'))['amount__sum'] or 0
        supplier_pay = Supplier_Buy_Pay.objects.filter(supplier__id=kwrags.get('id'),pay=True).aggregate(Sum('amount'))['amount__sum'] or 0
        
        supplier_baki = supplier_buy - supplier_pay
        contex = {
            'supplier': supplier,
            'supplier_buys' : supplier_buys,
            'supplier_pays' : supplier_pays,
            'supplier_buy' : supplier_buy,
            'supplier_pay' : supplier_pay ,
            'supplier_baki' : supplier_baki,
        }
        return render(request, "supplier_details.html",contex)

class CustomerFormView(generic.CreateView):
    form_class = CustomerForm
    template_name = 'customer_form.html'
    success_url = reverse_lazy('shop:home')
    
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.user = self.request.user
        self.obj.save()
        return super().form_valid(form)

class SupplierFormView(generic.CreateView):
    form_class = SupplierForm
    template_name = 'supplier_form.html'
    success_url = reverse_lazy('shop:home')
    
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.user = self.request.user
        self.obj.save()
        return super().form_valid(form)


class MonthlyCostView(generic.View):
    def get(self, request, *args, **kwrags):
        this_month = date.today().month
        cost_cash = Cash.objects.all().filter(cost=True,user=request.user,date__month=this_month).aggregate(Sum('amount'))['amount__sum']
        costs = Cash.objects.all().filter(cost=True,user=request.user,date__month=this_month)
        if 'month' in request.GET:
            name = request.GET.get('month')
            if name!='':
                year = name[0:4]
                month = name[5:]
                cost_cash = Cash.objects.all().filter(cost=True,user=request.user, date__month=month , date__year = year).aggregate(Sum('amount'))['amount__sum']
                costs = Cash.objects.all().filter(cost=True,user=request.user,date__month=month , date__year = year)
                contex = {
                    'cost_cash' : cost_cash,
                    'costs' : costs
                }
                return render(request, 'monthlycost.html', contex)
                
        contex = {
            'cost_cash' : cost_cash,
            'costs' : costs
        }
        return render(request, 'monthlycost.html', contex)


class MonthlyBakiView(generic.View):
    def get(self, request, *args, **kwrags):
        # old calculation
        all_baki = Customer_Cost_Pay.objects.all().filter(user=request.user,cost=True).aggregate(Sum('amount'))['amount__sum'] or 0
        all_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_baki_all = all_baki - all_pay
        # monthly calculation
        monthly_baki = Customer_Cost_Pay.objects.all().filter(user=request.user,cost=True,date__month = date.today().month ).aggregate(Sum('amount'))['amount__sum'] or 0
        monthly_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True,date__month = date.today().month ).aggregate(Sum('amount'))['amount__sum'] or 0
        total_baki = monthly_baki - monthly_pay
        # old calculation final result
        old_baki = total_baki_all - total_baki
        
        if 'month' in request.GET:
            name = request.GET.get('month')
            year = name[0:4]
            month = name[5:]
            # monthly calculation
            monthly_baki = Customer_Cost_Pay.objects.all().filter(user=request.user,cost=True,date__month = month ).aggregate(Sum('amount'))['amount__sum']
            monthly_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True,date__month = month ).aggregate(Sum('amount'))['amount__sum']
            total_baki = monthly_baki - monthly_pay

            this_to_today_baki = Customer_Cost_Pay.objects.all().filter(user=request.user,cost=True,date__month__gte = month , date__month__lte=date.today().month ).aggregate(Sum('amount'))['amount__sum']
            this_to_today_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True,date__month__gte = month , date__month__lte=date.today().month ).aggregate(Sum('amount'))['amount__sum']
            this_to_today_total = this_to_today_baki - this_to_today_pay
            # old calculation
            all_baki = Customer_Cost_Pay.objects.all().filter(user=request.user,cost=True).aggregate(Sum('amount'))['amount__sum']
            all_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True).aggregate(Sum('amount'))['amount__sum']
            total_baki_old = all_baki - all_pay
            # old calculation final result
            old_baki = total_baki_old - this_to_today_total
            total_baki_all = old_baki + total_baki
            contex = {
                'old_baki' : old_baki,
                'monthly_baki' : monthly_baki,
                'monthly_pay' : monthly_pay,
                'total_baki_all' : total_baki_all,
                
            }
            return render(request, 'monthlybaki.html', contex)

        contex = {
            'old_baki' : old_baki,
            'monthly_baki' : monthly_baki,
            'monthly_pay' : monthly_pay,
            'total_baki_all' : total_baki_all,
            
        }
        return render(request, 'monthlybaki.html', contex)

class MonthlyCashView(generic.View):
    def get(self, request, *args, **kwrags):
        cash_sell = Cash.objects.all().filter(sell_cash=True,user=request.user,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        customer_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        buy_cash = Cash.objects.all().filter(buy=True,user=request.user,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        supplier_pay = Supplier_Buy_Pay.objects.all().filter(user=request.user,pay=True,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        cost =  Cash.objects.all().filter(cost=True,user=request.user,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = cash_sell + customer_pay - buy_cash - supplier_pay - cost
        
        if 'month' in request.GET:
            name = request.GET.get('month')
            year = name[0:4]
            month = name[5:] 
            cash_sell = Cash.objects.all().filter(sell_cash=True,user=request.user,date__month = month).aggregate(Sum('amount'))['amount__sum']
            customer_pay = Customer_Cost_Pay.objects.all().filter(user=request.user,pay=True,date__month = month).aggregate(Sum('amount'))['amount__sum']
            buy_cash = Cash.objects.all().filter(buy=True,user=request.user,date__month = month).aggregate(Sum('amount'))['amount__sum']
            supplier_pay = Supplier_Buy_Pay.objects.all().filter(user=request.user,pay=True,date__month = month).aggregate(Sum('amount'))['amount__sum']
            cost =  Cash.objects.all().filter(cost=True,user=request.user,date__month = month).aggregate(Sum('amount'))['amount__sum']
            balance = cash_sell + customer_pay - buy_cash - supplier_pay - cost
            contex = {  
                'cash_sell':cash_sell,
                'customer_pay':customer_pay,
                'buy_cash': buy_cash,
                'supplier_pay':supplier_pay,
                'cost' : cost,
                'balance': balance
            }
            return render(request, 'monthlycash.html', contex)
            
        contex = {  
            'cash_sell':cash_sell,
            'customer_pay':customer_pay,
            'buy_cash': buy_cash,
            'supplier_pay':supplier_pay,
            'cost' : cost,
            'balance': balance
        }
        return render(request, 'monthlycash.html', contex)

class MonthlyBuySellView(generic.View):
    def get(self, request, *args, **kwrags):
        cash_sell = Cash.objects.all().filter(sell_cash=True,user=request.user,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        customer_sell = Customer_Cost_Pay.objects.all().filter(user=request.user, cost=True, date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        cash_buy = Cash.objects.all().filter(buy=True,user=request.user,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        supplier_buy = Supplier_Buy_Pay.objects.all().filter(user=request.user,buy=True,date__month = date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = cash_sell + customer_sell - cash_buy - supplier_buy
        
        if 'month' in request.GET:
            name = request.GET.get('month')
            year = name[0:4]
            month = name[5:] 
            cash_sell = Cash.objects.all().filter(sell_cash=True,user=request.user,date__month = month).aggregate(Sum('amount'))['amount__sum']
            customer_sell = Customer_Cost_Pay.objects.all().filter(user=request.user, cost=True, date__month = month).aggregate(Sum('amount'))['amount__sum']
            cash_buy = Cash.objects.all().filter(buy=True,user=request.user,date__month = month).aggregate(Sum('amount'))['amount__sum']
            supplier_buy = Supplier_Buy_Pay.objects.all().filter(user=request.user,buy=True,date__month = month).aggregate(Sum('amount'))['amount__sum']
            balance = cash_sell + customer_sell - cash_buy - supplier_buy
            contex = {  
                'cash_sell':cash_sell,
                'customer_sell' : customer_sell,
                'cash_buy' : cash_buy,
                'supplier_buy' : supplier_buy,
                'balance' : balance
            }
            return render(request, 'monthlybuysell.html', contex)

        contex = {  
            'cash_sell':cash_sell,
            'customer_sell' : customer_sell,
            'cash_buy' : cash_buy,
            'supplier_buy' : supplier_buy,
            'balance' : balance
        }
        return render(request, 'monthlybuysell.html', contex)