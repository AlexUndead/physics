import time
import unittest
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from .decorators import registration_user, autorization_user


class NewVisitorTest(LiveServerTestCase):
    '''тест нового посетителя'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Chrome('/var/www/html/Projects/selenium-drivers/chrome/80/chromedriver')

    def tearDown(self):
        '''демонтаж'''
        self.browser.quit()

    @registration_user
    def test_register_user(self) -> None:
        '''регистрация пользователя'''

        # Алексей убедился что он находится на странице успешной регистрации
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Вы успешно зарегистрировались', header_text)

    @registration_user
    @autorization_user
    def test_login_user(self) -> None:
        """авторизация пользователя"""

        # Алексей убедился что он успешно авторизовался
        user_account_link = self.browser.find_element_by_id('user-account-link')
        self.assertTrue(user_account_link)


    @registration_user
    @autorization_user
    def test_change_user_personal_data(self) -> None:
        """изменение настроек пользователя"""
        class UserPersonalData(Enum):
            """Личные измененные данные пользователя"""
            id_first_name = 'ChangedName'
            id_last_name = 'ChangedSurname'
            id_email = 'change@email.ru'

        # Алексей решин изменить свои пользовательские настройки
        # в личном кабинете

        # Он зашел в личный кабинет
        self.browser.find_element_by_id('user-account-link').click()

        # Изменил настройки
        for name, class_name in UserPersonalData.__members__.items():
            change_user_setting_input = self.browser.find_element_by_id(name)
            change_user_setting_input.send_keys(class_name.value)

        # Нажал кнопку "Сохранить настройки"
        self.browser.find_element_by_id('change-user-account-settings-form-submit').click()

        # Убедился что настройки сохранились
        user_account_messages = self.browser.find_element_by_id('user-account-messages')
        self.assertEqual('Ваши данные успешно сохраненны!', user_account_messages.text)
        
        
