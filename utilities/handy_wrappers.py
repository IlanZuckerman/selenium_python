import inspect, time, os
from selenium.webdriver.common.by import By
from traceback import print_stack


class HandyWrappers():

    def __init__(self, driver):
        self.driver = driver


    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        elif locatorType == "tagname":
            return By.TAG_NAME
        else:
            print("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            print("Element Found: %s %s " % (locator, locatorType))
        except:
            print("Element not found: %s %s " % (locator, locatorType))
        return element

    def isElementPresent(self, locator, locatorType='id'):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                print("Element Found: %s %s " % (locator, locatorType))
                return True
            else:
                print("Element not found: %s %s " % (locator, locatorType))
                return False
        except:
            print("Element not found")
            return False

