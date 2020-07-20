from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from enum import Enum
import time
import unittest

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):
    '''тест нового посетителя'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Chrome('/var/www/html/Projects/selenium-drivers/chrome/80/chromedriver')

    def tearDown(self):
        '''демонтаж'''
        self.browser.quit()

    def test_register_user(self):
        '''регистрация пользователя'''

        class UserPersonalData(Enum):
            id_username = 'TEST'
            id_email = 'test@test.ru'
            id_first_name = 'TestName'
            id_last_name = 'TestSurname'
            id_password1 = '305712bb'
            id_password2 = '305712bb'

        # Алексей слышал про новый замечательный портал по физике.
        # Он решил зайти на этот сайт
        self.browser.get(self.live_server_url)

        # И попробовать зарегистрироваться на нем
        register_link = self.browser.find_element_by_id('register-link')
        register_link.send_keys(Keys.ENTER)
         
        for name, class_name in UserPersonalData.__members__.items():
            register_input = self.browser.find_element_by_id(name)
            register_input.send_keys(class_name.value)

        register_submit = self.browser.find_element_by_id('register-submit')
        register_submit.send_keys(Keys.ENTER)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Вы успешно зарегистрировались', header_text)

