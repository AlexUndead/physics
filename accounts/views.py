from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from accounts.models import UserProfile
from accounts.forms import CustomRegisterForm, UploadAvatarForm
from accounts.serializers import AccountSettingsDetailSerializer
from accounts.decorators.views import redirect_not_registered_user
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response as RestframeworkResponse
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class CustomRegisterView(FormView):
    form_class = CustomRegisterForm
    success_url = '/accounts/success_register/'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserAccountSettingsView(View):
    """
    Страница настроект пользовательского аккаунта
    """

    @redirect_not_registered_user('login')
    def get(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user.id)
        except UserProfile.DoesNotExist:
            user_profile = None

        try:
            user = User.objects.get(id=request.user.id)
            data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
        except User.DoesNotExist:
            pass

        user_form = CustomRegisterForm(data)

        return render(request, 'user_account_settings.html', {'user_profile': user_profile, 'user_form': user_form})


class CustomerLoginView(LoginView):
    """
    Если пользователь зарегистрирован перенаправляет
    на страницу настроек
    """

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('user_account_settings')
        else:
            return super().get(request, *args, **kwargs)


def success_register(request):
    return render(request, 'success_register.html', context={})


class UploadAvatarView(View):
    """Страница загрузки аватарки для пользовотельских настроек"""

    def post(self, request):
        data = {
            'user': request.user.id
        }

        try:
            user_profile = UserProfile.objects.get(user=request.user.id)
        except UserProfile.DoesNotExist:
            user_profile = None

        form = UploadAvatarForm(data=data, files=request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()

        return redirect('account_settings')


class UserAccountSettingsChange(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSettingsDetailSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def post(self, request: HttpRequest, format=None) -> RestframeworkResponse:
        """Изменение данных пользователя"""
        status = 'success'
        message = 'Ваши данные сохранены успешно!'
        user = User.objects.get(pk=request.user.id)

        if self._has_differences_user_setting(request, user):
            self._update_user_setting(request, user)
        else:
            status = 'info'
            message = 'Ваши данные ничем не отличаются от прежних.'

        return RestframeworkResponse({
            'status':status, 
            'message':message,
        })

    def _update_user_setting(self, request:HttpRequest, user: User) -> None:
        """Обновление настроек пользователя"""
        user.email=request.data['email']
        user.first_name=request.data.get('first_name', '')
        user.last_name=request.data.get('last_name', '')
        user.save(force_update=True)

    def _has_differences_user_setting(self, request: HttpRequest, user: User) -> bool:
        """Проверка отличий настроек пользователя"""
        
        return any(
            request.data.get(user_setting, '') != getattr(user, user_setting)
            for user_setting in ['email', 'first_name', 'last_name']
        )
