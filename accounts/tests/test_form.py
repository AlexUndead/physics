from .base import AccountsBaseTest
from accounts.forms import UserSettingsForm


class AccountsChangeUserSettingsFormTest(AccountsBaseTest):
    """класс тестов для формы смены пользовательских настроек"""
    def setUp(self) -> None:
        self._create_user()

    def test_form_success_save_settings(self):
        """тест: форма успешно сохраняет настройки пользователя"""
        form = UserSettingsForm(
            data={
                'email': self.CHANGE_EMAIL,
                'first_name': self.CHANGE_FIRST_NAME,
                'last_name': self.CHANGE_LAST_NAME,
            },
            instance=self.user_model.objects.first()
        )

        new_user_settings = form.save()

        self.assertEqual(new_user_settings, self.user_model.objects.get(id=1))
        self.assertEqual(new_user_settings.email, self.CHANGE_EMAIL)

    def test_form_validation_for_empty_email(self):
        """тест: валидации формы с пустым email"""
        form = UserSettingsForm(
            data={'email': ''},
            instance=self.user_model.objects.first()
        )

        self.assertFalse(form.is_valid())
        any(self.assertEqual(error, 'Это поле обязательно.') for error in form.errors['email'])

    def test_form_validation_for_not_correct_email(self):
        """тест: валидации формы с некорректным email"""
        form = UserSettingsForm(
            data={'email': 'alex@test'},
            instance=self.user_model.objects.first()
        )

        self.assertFalse(form.is_valid())
        any(
            self.assertEqual(error, 'Введите корректный адрес электронной почты.') 
            for error in form.errors['email']
        )
