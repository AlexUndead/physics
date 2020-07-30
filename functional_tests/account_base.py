import time
import unittest
from typing import Dict
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.conf import settings
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

User = get_user_model()
USER_NAME = 'user_name'
USER_PASSWORD = 'user_password'
USER_EMAIL = 'user_email'
USER_FIRSTNAME = 'user_firstname'
USER_LASTNAME = 'user_lastname'


class UserAccountTest(LiveServerTestCase):
    '''тест личного кабинета пользователя'''

    def setUp(self) -> None:
        '''установка'''
        self.browser = webdriver.Chrome('/var/www/html/Projects/selenium-drivers/chrome/80/chromedriver')

    def tearDown(self) -> None:
        '''демонтаж'''
        #self.browser.quit()
        User.objects.all().delete()

    def test_login_user(self) -> None:
        """авторизация пользователя"""
        self._open_main_page_as_authorized()

        # Алексей убедился что он успешно авторизовался
        user_account_link = self.browser.find_element_by_id('user-account-link')
        self.assertTrue(user_account_link)


    def test_change_user_personal_data(self) -> None:
        """изменение настроек пользователя"""
        class UserPersonalData(Enum):
            """Личные измененные данные пользователя"""
            id_first_name = 'user_changed_name'
            id_last_name = 'user_changed_surname'
            id_email = 'change@email.ru'

        self._open_main_page_as_authorized()

        # Алексей решин изменить свои пользовательские настройки
        # в личном кабинете

        # Он зашел в личный кабинет
        self.browser.find_element_by_id('user-account-link').click()

        # Изменил настройки
        for name, class_name in UserPersonalData.__members__.items():
            change_user_setting_input = self.browser.find_element_by_id(name)
            change_user_setting_input.clear()
            change_user_setting_input.send_keys(class_name.value)

        # Нажал кнопку "Сохранить настройки"
        self.browser.find_element_by_id('change-user-account-settings-form-submit').click()

        # Убедился что настройки сохранились
        user_account_messages = self.browser.find_element_by_id('user-account-messages')
        self.assertEqual('Ваши данные успешно сохраненны!', user_account_messages.text)

    def _open_main_page_as_authorized(self) -> None:
        """открытие гланой страницы авторизованным пользователем"""
        self.browser.get(self.live_server_url + '/404-non-existent/')
        self.browser.add_cookie(self._create_user_session_cookie())
        self.browser.refresh()
        self.browser.get(self.live_server_url)
        
    def _create_user_session_cookie(self) -> Dict[str, str]:
        """создание сесиии авторизованного пользователя"""
        user = User.objects.create_user(
            username=USER_NAME,
            password=USER_PASSWORD,
            email=USER_EMAIL,
            first_name=USER_FIRSTNAME,
            last_name=USER_LASTNAME,
        )
        
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        cookie = {
            'name': settings.SESSION_COOKIE_NAME,
            'value': session.session_key,
            'secure': False,
            'path': '/',
        }

        return cookie
