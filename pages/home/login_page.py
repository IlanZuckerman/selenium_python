from base.selenium_driver import SeleniumDriver
import utilities.custom_logger as cl
import logging, time

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


    def login(self, username='', password=''):
        # self.clickWelcomeAdminField()
        self.enterPasswordField(password)
        self.enterUsernameField(username)
        self.clickSubmitButton()

    def verifyLoginSuccesfull(self):
        # self.assertIn('Red Hat Virtualization Manager Web Administration', self.driver.title, 'Title is not as expected')
        element = self.waitForElement('id-compute')
        return element is not None

    def verifyLoginFailed(self):
        # TODO: convert this to text inside the message
        result = self.isElementPresent("//div[@class='alert alert-warning alert-dismissable']", 'xpath')
        return result

    def verifyTitle(self):
        time.sleep(2)
        if 'Red Hat Virtualization Manager Web Administration' in self.getTitle():
            return True
        else:
            return False