import time
from enum import Enum
from typing import Callable, TypeVar
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 5
RETURN = TypeVar('RETURN')


def autorization_user(func: Callable[..., RETURN]) -> Callable[..., None]:
    """Авторизация пользователя"""
    def wrapper(self, *args, **kwargs) -> None:
        class UserPersonalData(Enum):
            """Личные данные пользователя"""
            id_username = 'Alexey'
            id_password = '305712bb'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('login-link').click()
        for name, class_name in UserPersonalData.__members__.items():
            autorization_input = self.browser.find_element_by_id(name)
            autorization_input.send_keys(class_name.value)
        self.browser.find_element_by_id('login-form-submit').click()
        func(self, *args, **kwargs)

    return wrapper

def registration_user(func: Callable[..., RETURN]) -> Callable[..., None]:
    """Регистрация пользователя"""
    def wrapper(self, *args, **kwargs) -> None:
        class UserPersonalData(Enum):
            """Личные данные пользователя"""
            id_username = 'Alexey'
            id_email = 'test@email.ru'
            id_first_name = 'TestName'
            id_last_name = 'TestSurname'
            id_password1 = '305712bb'
            id_password2 = '305712bb'

        self.browser.get(self.live_server_url)
        register_link = self.browser.find_element_by_id('register-link')
        register_link.send_keys(Keys.ENTER)
        for name, class_name in UserPersonalData.__members__.items():
            register_input = self.browser.find_element_by_id(name)
            register_input.send_keys(class_name.value)
        self.browser.find_element_by_id('register-submit').click()
        func(self, *args, **kwargs)

    return wrapper

