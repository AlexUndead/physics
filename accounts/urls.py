from django.contrib.auth import views
from django.urls import path
from . import views as custom_views

urlpatterns = [
    path('account_settings/', custom_views.AccountSettingsView.as_view(), name='account_settings'),
    path('login/', custom_views.CustomerLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', custom_views.RegisterFormView.as_view(), name='register'),
    path('success_register/', custom_views.success_register, name='success_register'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
