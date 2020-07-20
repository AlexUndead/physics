from django.shortcuts import redirect

def redirect_not_registered_user(redirect_url):
    '''Перенаправление не зарегистрированного пользователя'''
    def first_wrapper(func):
        def second_wrapper(self, request, *args, **kwargs):
            if not self.request.user.is_authenticated:
                return redirect(redirect_url)
            return func(self, request, *args, **kwargs)

        return second_wrapper
    return first_wrapper

