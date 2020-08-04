from django.contrib.auth import views
from django.urls import path
from accounts import views as custom_views

urlpatterns = [
    path('settings/upload_avatar/', custom_views.UploadAvatarView.as_view(), name='upload_avatar'),
    path('settings/', custom_views.UserAccountSettingsView.as_view(), name='user_account_settings'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', custom_views.CustomRegisterView.as_view(), name='register'),
    path('success_register/', custom_views.success_register, name='success_register'),
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
