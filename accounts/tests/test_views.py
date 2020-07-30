from enum import Enum
from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()
TEMPORARY_USERNAME = 'temporary_username'
TEMPORARY_PASSWORD = 'temporary_password'
TEMPORARY_EMAIL = 'temporary@gmail.ru'
TEMPORARY_FIRSTNAME = 'first_temporary_name'
TEMPORARY_LASTNAME = 'last_temporary_name'
CHANGE_EMAIL = 'change@gmail.ru'
CHANGE_FIRST_NAME = 'first_change_name'
CHANGE_LAST_NAME = 'last_change_name'
ACCOUNT_SETTINGS_CHANGE_URL = '/accounts/settings/change/'


class AuthenticatedPartTest(TestCase):
    """тест разделов сайта для аутентифицированных пользователей"""
    def setUp(self) -> None:
        self._create_user()
        self.client.login(
            username=TEMPORARY_USERNAME, 
            password=TEMPORARY_PASSWORD
        )

    def test_uses_account_template(self) -> None:
        """тест: используется шаблон аккаунта"""
        response = self.client.get('/accounts/settings/')
        self.assertTemplateUsed(response, 'user_account_settings.html')

    def test_displays_only_items_for_that_user(self) -> None:
        """тест: отображение правильных настроек пользователя"""
        response = self.client.get('/accounts/settings/')
        for user_account_setting in [TEMPORARY_EMAIL, TEMPORARY_FIRSTNAME, TEMPORARY_LASTNAME]:
            self.assertContains(response, user_account_setting)

    def test_correct_status_code_response(self) -> None:
        """тест: корректность кода ответа запроса"""
        response = self._send_post_on_account_settings_change()
        
        self.assertRedirects(response, '/accounts/settings/')

    def test_display_correct_settings_after_change(self) -> None:
        """
        тест: отображение правильных настроек аккауна
        после изменений
        """
        class UserPersonalData(Enum):
            """Личные измененные данные пользователя"""
            first_name = CHANGE_FIRST_NAME
            last_name = CHANGE_LAST_NAME
            email = CHANGE_EMAIL

        response = self._send_post_on_account_settings_change(
            user_email=CHANGE_EMAIL, 
            user_first_name=CHANGE_FIRST_NAME, 
            user_last_name=CHANGE_LAST_NAME
        )
        user = User.objects.get(id=1)

        for user_account_setting in UserPersonalData:
            self.assertEqual(user.__getattribute__(user_account_setting.name), user_account_setting.value)
        

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
            ACCOUNT_SETTINGS_CHANGE_URL,
            data={
                'email': user_email, 
                'first_name': user_first_name, 
                'last_name': user_last_name,
            }
        )

    def _create_user(self) -> None:
        """создание пользователя"""
        User = get_user_model()
        User.objects.create_user(
            TEMPORARY_USERNAME, 
            TEMPORARY_EMAIL, 
            TEMPORARY_PASSWORD, 
            first_name=TEMPORARY_FIRSTNAME, 
            last_name=TEMPORARY_LASTNAME,
        )

