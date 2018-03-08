import inspect, time, os, logging

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from traceback import print_stack

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl


class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        fileName = resultMessage + '.' + str(round(time.time() * 1000)) + '.png'
        screenshotDirectory = '../screenshot/'
        relativeFileName = screenshotDirectory + fileName.replace(" ", "")
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists((destinationDirectory)):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info('Screenshot saved to directory: ' + destinationFile)
        except:
            self.log.error('### Exception Occured')
            print_stack()

    def getTitle(self):
        return self.driver.title

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
        elif locatorType == "classname":
            return By.CLASS_NAME
        elif locatorType == "linktext":
            return By.LINK_TEXT
        elif locatorType == "tagname":
            return By.TAG_NAME
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False


    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found: %s %s " % (locator, locatorType))
        except:
            self.log.info("Element not found: %s %s " % (locator, locatorType))
        return element

    def getElements(self, locator, locatorType="id"):
        elements = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info("Element Found: %s %s " % (locator, locatorType))
        except:
            self.log.info("Element not found: %s %s " % (locator, locatorType))
        return elements


    def elementClick(self, locator, locatorType="id"):
        tmp = self.waitForElement(locator, locatorType)
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def elementClickShift(self, locator, locatorType="id"):
        # TODO: add a step to check if line already selected, and select it only if its not.
        try:
            elem = self.getElement(locator, locatorType)
            ActionChains(self.driver).key_down(Keys.CONTROL).click(elem).key_up(Keys.CONTROL).perform()
            time.sleep(1)
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()


    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.clear()
            element.click()
            element.send_keys(data)
            self.log.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()


    def isElementPresent(self, locator, byType):
        try:
            element = self.driver.find_element(byType, locator)
            if element is not None:
                self.log.info("Element Found: %s %s " % (locator, byType))
                return True
            else:
                self.log.info("Element not found: %s %s " % (locator, byType))
                return False
        except:
            self.log.info("Element not found")
            return False


    def waitForElement(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        time.sleep(2)
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element %s  %s appeared on the web page" % (locator, locatorType))
        except:
            self.log.info("Element %s  %s not appeared on the web page" % (locator, locatorType))
            print_stack()
        return element

    def waitForElementToDissapear(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to dissapear")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            wait.until_not(EC.presence_of_element_located((byType, locator)))
            self.log.info("Element %s  %s disappeared on the web page" % (locator, locatorType))
        except:
            self.log.info("Element %s  %s not disappeared on the web page" % (locator, locatorType))
            print_stack()


    def write_delta_to_csv(self, suit_run_path, file_name, delta):
        with open(os.path.join(suit_run_path, file_name), 'w') as full_path:
            full_path.write(str(delta))
            self.log.info('wrote to ' + str(full_path))


    def measure_time(self, locator, bytype, start_time, timeout, suit_run_path):
        exit_condition = False
        while not exit_condition:
            exit_condition = self.isElementPresent(locator, bytype)

            self.log.info('Measuring time for locator: %s type: %s' % (locator, bytype))
            time.sleep(1)
            if (time.time() - start_time) > timeout:
                self.fail('It took more than %s seconds for element to appear: %s %s' % (timeout, locator, bytype))

        delta = time.time() - start_time
        self.write_delta_to_csv(suit_run_path, inspect.stack()[0][3], delta)
        self.log.info('It took %s seconds for element to appear: %s %s' % (delta, locator, bytype))

    def execute_js_search(self, elem):
        elem = self.getElement(elem)
        my = 'name=selenium* and status=rebootinprogress'
        self.driver.execute_script("document.getElementById('SearchPanelView_searchStringInput').value=''")
        self.driver.execute_script("document.getElementById('SearchPanelView_searchStringInput').value='name=selenium* and status=rebootinprogress'")
        self.driver.execute_script("document.getElementById('SearchPanelView_searchButton').click()")

    def scroll_down(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);",element)
        var = "//li/a[contains(text(), 'L3_nested_2')]"
        # self.driver.execute_script("document.getElementByXpath('%s').click()" % var)