from enum import Enum
from typing import Callable, TypeVar
from selenium.webdriver.common.keys import Keys

Return = TypeVar('Return')


def registration_user(func: Callable[..., Return]) -> Callable[..., None]:
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
        register_submit = self.browser.find_element_by_id('register-submit')
        register_submit.send_keys(Keys.ENTER)
        func(self, *args, **kwargs)

    return wrapper
