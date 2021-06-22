from django.urls import path
from django.contrib.auth import views as auth_views
app_name = "accounts"
from accounts import views
from django.urls import reverse_lazy


urlpatterns = [
    
    path('profileupdate/<int:id>', views.ProfileUpdateView.as_view() , name='profileupdate'),
    
    path('register/', views.Register_User.as_view(), name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html' , success_url=reverse_lazy('shop:home')), name='change_password'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html' , success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html' , success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]