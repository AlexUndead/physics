from typing import Callable, Optional, TypeVar
from django.shortcuts import redirect

T = TypeVar('T')

def redirect_not_registered_user(redirect_url: Optional[str]) -> Callable[[T], T]:
    '''Перенаправление незарегистрированного пользователя'''
    def first_wrapper(func: T) -> T:
        def second_wrapper(self, *args, **kwargs):
            if not self.request.user.is_authenticated:
                return redirect(redirect_url)
            return func(self, *args, **kwargs)

        return second_wrapper
    return first_wrapper

