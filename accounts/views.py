from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = '/accounts/success_register/'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


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
        return render(request, 'account_settings.html', {})


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
