"""
@package base

WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
import traceback
from selenium import webdriver

class WebDriverFactory():

    def __init__(self, username, password, browser, engineUrl):
        """
        Inits WebDriverFactory class

        Returns: None
        """
        self.username = username
        self.password = password
        self.browser = browser
        self.engineUrl = engineUrl
    """
    Set chrome driver and iexplorer environment based on OS

    chromedriver = "C:/.../chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    self.driver = webdriver.Chrome(chromedriver)

    PREFERRED: Set the path on the machine where browser will be executed
    """

    def getWebDriverInstance(self):
        """
       Get WebDriver Instance based on the browser configuration

        Returns:
            'WebDriver Instance'
        """
        # baseURL = "https://b01-h21-r620.rhev.openstack.engineering.redhat.com"
        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            # Set chrome driver (look above)
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()
        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(5)
        # Maximize the window
        # driver.maximize_window()
        # Loading browser with App URL
        driver.get(self.engineUrl)
        return driver