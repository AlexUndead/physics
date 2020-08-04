from enum import Enum
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .base import AccountsBaseTest



class AuthenticatedPartTest(AccountsBaseTest):
    """тест разделов сайта для аутентифицированных пользователей"""
    def setUp(self) -> None:
        self._create_user()
        self.client.login(
            username=self.TEMPORARY_USERNAME, 
            password=self.TEMPORARY_PASSWORD
        )

    def test_uses_account_template(self) -> None:
        """тест: используется шаблон аккаунта"""
        response = self.client.get('/accounts/settings/')
        self.assertTemplateUsed(response, 'user_account_settings.html')

    def test_displays_only_items_for_that_user(self) -> None:
        """тест: отображение правильных настроек пользователя"""
        response = self.client.get('/accounts/settings/')
        for user_account_setting in [
                self.TEMPORARY_EMAIL, 
                self.TEMPORARY_FIRSTNAME, 
                self.TEMPORARY_LASTNAME
            ]:
            self.assertContains(response, user_account_setting)

    def test_correct_status_code_response(self) -> None:
        """тест: корректность кода ответа запроса"""
        response = self._send_post_on_account_settings_change(
            user_email=self.CHANGE_EMAIL, 
            user_first_name=self.CHANGE_FIRST_NAME, 
            user_last_name=self.CHANGE_LAST_NAME
        )
        
        self.assertRedirects(response, '/accounts/settings/', status_code=301)

    def test_correct_user_message_after_success_change_settings(self) -> None:
        """
        тест: правильное сообщенеие 
        после успешного изменения настроек пользователя
        """
        response = self._send_post_on_account_settings_change(
            user_email=self.CHANGE_EMAIL, 
            user_first_name=self.CHANGE_FIRST_NAME, 
            user_last_name=self.CHANGE_LAST_NAME
        )

        any(
            self.assertEqual(m.message, 'Ваши данные успешно сохранены!') for m 
            in list(get_messages(response.wsgi_request))
        )

    def test_display_correct_settings_after_change(self) -> None:
        """
        тест: отображение правильных настроек аккауна
        после изменений
        """
        class UserPersonalData(Enum):
            """Личные измененные данные пользователя"""
            first_name = self.CHANGE_FIRST_NAME
            last_name = self.CHANGE_LAST_NAME
            email = self.CHANGE_EMAIL

        response = self._send_post_on_account_settings_change(
            user_email=self.CHANGE_EMAIL, 
            user_first_name=self.CHANGE_FIRST_NAME, 
            user_last_name=self.CHANGE_LAST_NAME
        )
        user = self.user_model.objects.get(id=1)

        for user_account_setting in UserPersonalData:
            self.assertEqual(user.__getattribute__(user_account_setting.name), user_account_setting.value)
