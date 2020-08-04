from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import UserSettings


class CustomRegisterForm(UserCreationForm):
    """Кастомная форма регистрации"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UploadAvatarForm(ModelForm):
    """Форма загрузки аватарки"""

    class Meta:
        model = UserSettings
        fields = ('avatar', 'user')


class UserSettingsForm(ModelForm):
    """Форма изенения настроек пользователя"""
    email = forms.EmailField(
            required=True,
            widget=forms.EmailInput(attrs={'class': 'form-control input-lg'})
    )
    first_name = last_name = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control input-lg'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
