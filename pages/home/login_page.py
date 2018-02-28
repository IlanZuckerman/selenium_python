from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from utilities.handy_wrappers import HandyWrappers
from selenium import webdriver
from selenium.webdriver.common.by import By
from base.selenium_driver import SeleniumDriver
import utilities.custom_logger as cl
import logging

class LoginPage(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    _welcome_webadmin_field = 'WelcomePage_webadmin'
    _username_field = 'username'
    _password_field = 'password'
    _submit_btn = '//button[@type="submit"]'


    def clickWelcomeAdminField(self):
        self.elementClick(self._welcome_webadmin_field)

    def enterUsernameField(self, username):
        self.sendKeys(username, self._username_field)

    def enterPasswordField(self, password):
        self.sendKeys(password, self._password_field)

    def clickSubmitButton(self):
        self.elementClick(self._submit_btn, locatorType='xpath')


    def login(self, username, password):
        # hw = HandyWrappers(self.driver)

        self.clickWelcomeAdminField()
        self.enterPasswordField(password)
        self.enterUsernameField(username)
        self.clickSubmitButton()
