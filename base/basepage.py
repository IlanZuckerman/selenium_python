"""
@package base

Base Page class implementation
It implements methods which are common to all the pages throughout the application

This class needs to be inherited by all the page classes
This should not be used by creating object instances

Example:
    Class LoginPage(BasePage)
"""
from selenium.webdriver.support.wait import WebDriverWait

from base.selenium_driver import SeleniumDriver
from traceback import print_stack
from utilities.util import Util
import pytest

class BasePage(SeleniumDriver):

    def __init__(self, driver):
        """
        Inits BasePage class

        Returns:
            None
        """
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    def verifyPageTitle(self, titleToVerify):
        """
        Verify the page Title

        Parameters:
            titleToVerify: Title on the page that needs to be verified
        """
        try:
            WebDriverWait(self.driver, 20).until(lambda x: titleToVerify in self.getTitle())
            actualTitle = self.getTitle()
            return self.util.verifyTextContains(actualTitle, titleToVerify)
        except:
            self.log.error("Failed to get page title")
            print_stack()
            return False

    def verifyAmountOfRowsInTable(self, expected_rows_amount, allowed_offset=3):
        """

        """
        try:
            WebDriverWait(self.driver, 30).until(lambda x: abs((len(self.getElements('//tr', 'xpath'))-1) - expected_rows_amount) <= allowed_offset)
            return True
        except:
            actualRowsAmount = len(self.getElements('//tr', 'xpath')) - 1  # minus one for ignoring header
            self.log.error("Amount of rows in the table is not as expected. Actual: %s Expected: %s Allowed offset: %s"
                           %(actualRowsAmount, expected_rows_amount, allowed_offset))
            print_stack()
            return None