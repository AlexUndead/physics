from django.test import TestCase


class AuthenticatedPartTest(TestCase):
    """тест разделов сайта для аутентифицированных пользователей"""

    def test_redirect_from_account_setting(self):
        """
        редирект неаутентифицированного пользователя со
        страниц настройки личного кабирена
        """
        response = self.client.get('/accounts/account_settings/')
        self.assertRedirects(response, '/accounts/login/')
