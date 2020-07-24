import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
from .decorators.registration_user import registration_user


class NewVisitorTest(LiveServerTestCase):
    '''тест нового посетителя'''

    def setUp(self):
        '''установка'''
        self.browser = webdriver.Chrome('/var/www/html/Projects/selenium-drivers/chrome/80/chromedriver')

    def tearDown(self):
        '''демонтаж'''
        self.browser.quit()

    @registration_user
    def test_register_user(self):
        '''регистрация пользователя'''

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Вы успешно зарегистрировались', header_text)
