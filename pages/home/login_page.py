from base.basepage import BasePage
import utilities.custom_logger as cl
import logging, time
from selenium.webdriver import ActionChains

class LoginPage(BasePage):

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


    def login(self, username='', password=''):
        self.enterPasswordField(password)
        self.enterUsernameField(username)
        self.clickSubmitButton()

    def verifyLoginSuccesfull(self):
        # self.assertIn('Red Hat Virtualization Manager Web Administration', self.driver.title, 'Title is not as expected')
        element = self.waitForElement('id-compute', timeout=30)
        return element is not None

    def verifyLoginFailed(self):
        # TODO: convert this to text inside the message
        result = self.isElementPresent("//div[@class='alert alert-warning alert-dismissable']", 'xpath')
        return result

    def verifyTitle(self):
        return self.verifyPageTitle('Red Hat Virtualization Manager Web Administration')

    def hover_over_login(self):
        element_to_hover = self.getElement(self._submit_btn, locatorType='xpath')
        ActionChains(self.driver).move_to_element(element_to_hover).perform()
