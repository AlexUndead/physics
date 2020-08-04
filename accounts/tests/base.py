from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth import get_user_model


class AccountsBaseTest(TestCase):
    user_model = get_user_model()
    TEMPORARY_USERNAME = 'temporary_username'
    TEMPORARY_PASSWORD = 'temporary_password'
    TEMPORARY_EMAIL = 'temporary@gmail.ru'
    TEMPORARY_FIRSTNAME = 'first_temporary_name'
    TEMPORARY_LASTNAME = 'last_temporary_name'
    CHANGE_EMAIL = 'change@gmail.ru'
    CHANGE_FIRST_NAME = 'first_change_name'
    CHANGE_LAST_NAME = 'last_change_name'
    ACCOUNT_SETTINGS_CHANGE_URL = '/accounts/settings/'

    """базовый класс тесто модуля accounts"""
    def _send_post_on_account_settings_change(
            self, 
            user_email:str = '', 
            user_first_name:str = '', 
            user_last_name:str = '',
        ) -> HttpResponse:
        """
        отправить POST запрос на страницу изменения настроек 
        аккаунта пользователя
        """
        return self.client.post(
            self.ACCOUNT_SETTINGS_CHANGE_URL,
            data={
                'email': user_email, 
                'first_name': user_first_name, 
                'last_name': user_last_name,
            }
        )

    def _create_user(self) -> None:
        """создание пользователя"""
        user = get_user_model()
        user.objects.create_user(
            self.TEMPORARY_USERNAME, 
            self.TEMPORARY_EMAIL, 
            self.TEMPORARY_PASSWORD, 
            first_name=self.TEMPORARY_FIRSTNAME, 
            last_name=self.TEMPORARY_LASTNAME,
        )
