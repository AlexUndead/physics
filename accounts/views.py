from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from accounts.models import UserProfile
from accounts.forms import CustomRegisterForm, UploadAvatarForm
from accounts.serializers import AccountSettingsDetailSerializer
from accounts.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

User = get_user_model()


class CustomRegisterView(FormView):
    form_class = CustomRegisterForm
    success_url = '/accounts/success_register/'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AccountSettingsView(View):
    """
    Страница настроект пользовательского аккаунта
    """

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            return super().dispatch(request, *args, **kwargs)

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

        return render(request, 'account_settings.html', {'user_profile': user_profile, 'user_form': user_form})


class CustomerLoginView(LoginView):
    """
    Если пользователь зарегистрирован перенаправляет
    на страницу настроек
    """

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account_settings')
        else:
            return super().dispatch(request, *args, **kwargs)


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


class AccountSettingsChangeView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSettingsDetailSerializer
    authentication_classes = (SessionAuthentication, )
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadOnly, )
