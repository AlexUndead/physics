from django.test import TestCase
from django.contrib.auth import get_user_model

TEMPORARY_USERNAME = 'temporary_username'
TEMPORARY_PASSWORD = 'temporary_password'
TEMPORARY_EMAIL = 'temporary@gmail.ru'
TEMPORARY_FIRSTNAME = 'first_temporary_name'
TEMPORARY_LASTNAME = 'last_temporary_name'
CHANGE_EMAIL = 'change@gmail.ru'
CHANGE_FIRSTNAME = 'first_change_name'
CHANGE_LASTNAME = 'last_change_name'


class AuthenticatedPartTest(TestCase):
    """тест разделов сайта для аутентифицированных пользователей"""
    def setUp(self):
        self._create_user()
        self.client.login(
            username=TEMPORARY_USERNAME, 
            password=TEMPORARY_PASSWORD
        )

    def test_redirect_from_login(self):
        """
        редирект аутентифицированного пользователя
        со страницы логина на страницу настроки кабинета
        """
        response = self.client.get('/accounts/login/')
        self.assertRedirects(response, '/accounts/settings/')

    def test_displays_only_items_for_that_user(self):
        """тест: отображение правильных настроек пользователя"""
        response = self.client.get('/accounts/settings/')
        for user_account_setting in [TEMPORARY_EMAIL, TEMPORARY_FIRSTNAME, TEMPORARY_LASTNAME]:
            self.assertContains(response, user_account_setting)

    def test_correct_status_code_response(self):
        """тест: тест корректного кода ответа запроса"""
        response = self.client.post(
                '/accounts/settings/change/',
                data={
                    'email': CHANGE_EMAIL, 
                    'first_name': CHANGE_FIRSTNAME, 
                    'last_name': CHANGE_LASTNAME,
                }
        )
        
        self.assertEqual(response.status_code, 200)

    def test_change_user_settings(self):
        """тест: успешное сохранение настроек пользователя"""
        response = self.client.post(
                '/accounts/settings/change/',
                data={
                    'email': CHANGE_EMAIL, 
                    'first_name': CHANGE_FIRSTNAME, 
                    'last_name': CHANGE_LASTNAME,
                }
        )
        
        self.assertEqual(response.json()['status'], 'success')

    def test_get_correct_status_after_transfer_user_settings_to_some_once(self):
        """
        тест: проверка статуса ответа после передачи настроек пользователя 
        совподающих с начальными настройками
        """
        response = self.client.post(
                '/accounts/settings/change/',
                data={
                    'email': TEMPORARY_EMAIL, 
                    'first_name': TEMPORARY_FIRSTNAME, 
                    'last_name': TEMPORARY_LASTNAME,
                }
        )
        
        self.assertEqual(
            response.json()['status'], 
            'info'
        )

    def test_get_correct_status_after_transfer_user_settings_with_empty_email(self):
        """тест: проверка статуса ответа предупреждющего о том что передан пустой email"""
        response = self.client.post(
                '/accounts/settings/change/',
                data={
                    'email': '', 
                }
        )
        
        self.assertEqual(
            response.json()['status'], 
            'warning'
        )

    def test_get_correct_status_after_transfer_user_settings_with_invalid_email(self):
        """тест: предупреждение о том что передан пустой email"""
        response = self.client.post(
                '/accounts/settings/change/',
                data={
                    'email': 'ivalid_email', 
                }
        )
        
        self.assertEqual(
            response.json()['status'], 
            'warning'
        )

    def _create_user(self):
        """создание пользователя"""
        User = get_user_model()
        User.objects.create_user(
            TEMPORARY_USERNAME, 
            TEMPORARY_EMAIL, 
            TEMPORARY_PASSWORD, 
            first_name=TEMPORARY_FIRSTNAME, 
            last_name=TEMPORARY_LASTNAME,
        )

