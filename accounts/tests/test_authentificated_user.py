from django.test import TestCase
from django.contrib.auth import get_user_model

TEMPORARY_USERNAME = 'temporary'
TEMPORARY_PASSWORD = 'temporary'
TEMPORARY_EMAIL = 'temporary@gmail.ru'


class AuthenticatedPartTest(TestCase):
    """тест разделов сайта для аутентифицированных пользователей"""
    def setUp(self):
        self.create_user()
        self.client.login(username=TEMPORARY_USERNAME, password=TEMPORARY_PASSWORD)

    def test_redirect_from_login(self):
        """
        редирект аутентифицированного пользователя
        со страницы логина на страницу настроки кабинета
        """
        response = self.client.get('/accounts/login/')
        self.assertRedirects(response, '/accounts/settings/')

    def create_user(self):
        """создание пользователя"""
        User = get_user_model()
        User.objects.create_user(TEMPORARY_USERNAME, TEMPORARY_EMAIL, TEMPORARY_PASSWORD)


