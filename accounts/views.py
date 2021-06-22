from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login
from .forms import CustomUserCreationForm , UserForm , ShopForm
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy

class Register_User(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('shop:home')
    
    def form_valid(self, form):
        self.user = form.save()
        self.user.refresh_from_db() 
        self.user.user_shop.shop_name = form.cleaned_data.get('shop_name')
        self.user.user_shop.phone = form.cleaned_data.get('phone')
        self.user.user_shop.address = form.cleaned_data.get('address')
        self.user.save()
        return super().form_valid(form)


class ProfileUpdateView(generic.View):
    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        shop_form = ShopForm(instance=request.user.user_shop)
        context = {
            'user_form': user_form,
            'shop_form': shop_form,
        }
        return render(request, 'profile.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST,instance=request.user)
        shop_form = ShopForm(request.POST, request.FILES, instance=request.user.user_shop)
        if user_form.is_valid() and shop_form.is_valid():
            user_form.save()
            shop_form.save()
            return redirect('shop:home')
        else:
            context = {
                'user_form': user_form,
                'shop_form': shop_form,
            }
            return render(request, 'profile.html', context)




