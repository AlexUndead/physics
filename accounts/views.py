from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import UserSettings
from accounts.forms import CustomRegisterForm, UploadAvatarForm, UserSettingsForm
from accounts.decorators.views import redirect_not_registered_user

User = get_user_model()


class CustomRegisterView(FormView):
    """Страница регистрации пользователя"""
    form_class = CustomRegisterForm
    success_url = '/accounts/success_register/'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserAccountSettingsView(LoginRequiredMixin, View):
    """Страница настроект пользовательского аккаунта"""
    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        user_profile, created = UserSettings.objects.get_or_create(user=user)
        form_data = {
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email
        }
        user_form = UserSettingsForm(form_data)

        return render(
            request, 
            'user_account_settings.html', 
            {'user_profile': user_profile, 'user_form': user_form}
        )


def success_register(request):
    return render(request, 'success_register.html', context={})


class UploadAvatarView(View):
    """Страница загрузки аватарки для пользовотельских настроек"""

    def post(self, request):
        data = {
            'user': request.user.id
        }

        try:
            user_profile = UserSettings.objects.get(user=request.user.id)
        except UserSettings.DoesNotExist:
            user_profile = None

        form = UploadAvatarForm(data=data, files=request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()

        return redirect('account_settings')


class UserAccountSettingsChange(LoginRequiredMixin, View):
    """Изменение настроек личного кабинета пользователя"""
    def post(self, request: HttpRequest) -> HttpResponse:
        user_form = UserSettingsForm(
            request.POST,
            instance=request.user
        )
        if user_form.is_valid():
            user_form.save()
        return redirect('user_account_settings')
