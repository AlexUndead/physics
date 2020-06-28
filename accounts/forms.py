from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import UserProfile


class CustomRegisterForm(UserCreationForm):
    """Кастомная форма регистрации"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UploadAvatarForm(ModelForm):
    """Форма загрузки аватарки"""

    class Meta:
        model = UserProfile
        fields = ('avatar', 'user')
