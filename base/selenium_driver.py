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
        self.start_time = 0
        self.end_time = 0


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
            self.log.warn("Locator type " + locatorType + " not correct/supported")
        return False


    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found: %s %s " % (locator, locatorType))
        except:
            self.log.warn("Element not found: %s %s " % (locator, locatorType))
        return element

    def getElements(self, locator, locatorType="id"):
        elements = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info("Element Found: %s %s " % (locator, locatorType))
        except:
            self.log.warn("Element not found: %s %s " % (locator, locatorType))
        return elements


    def elementClick(self, locator='', locatorType='id', element=None):
        try:
            if locator: # meaning that locator is not empty
                tmp = self.waitForElement(locator, locatorType)
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)

        except:
            self.log.warn("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def elementClickShift(self, locator='', locatorType='id', elem=None):
        try:
            if locator:
                elem = self.getElement(locator, locatorType)
            # parent = self.getElement(locator + '//parent::tr', locatorType)
            # parent_class_name = parent.get_attribute('class')
            # i noted then when a row already selected, its class attribute value consist of few white space delimmited
            # phrases such as 'GNEKTHVBHM GNEKTHVBJM'. so clicking on a row with only one phrase to avoid double click on
            # the same row.
            # TODO: Solve problem when clicking but row not sellected
            # if len(parent_class_name.split()) == 1:
            self.driver.execute_script("arguments[0].scrollIntoView();", elem)
            ActionChains(self.driver).key_down(Keys.SHIFT).click(elem).key_up(Keys.SHIFT).perform()
            time.sleep(1)
            self.log.info(" Shift Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warn("Cannot Shift click on the element with locator: " + locator + " locatorType: " + locatorType)
            # print_stack()


    def sendKeys(self, data, locator='', locatorType='id', element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.clear()
            element.send_keys(data)
            self.log.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)

            # element = self.getElement(locator, locatorType)
            # element.clear()
            # element.click()
            # element.send_keys(data)
            # self.log.info("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except:
            self.log.warn("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print_stack()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        """
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                self.log.debug("In locator condition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding text")
            text = element.text
            self.log.debug("After finding element, size is: " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementPresent(self, locator="", locatorType="id", element=None):
        """
        Check if element is present -> MODIFIED
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element present with locator: " + locator +
                              " locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        """
        Check if element is displayed
        Either provide element or a combination of locator and locatorType
        """
        isDisplayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not displayed with locator: " + locator +
                              " locatorType: " + locatorType)
            return isDisplayed
        except:
            print("Element not found")
            return False

    def webScroll(self, direction="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")


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
            self.log.warn("Element %s  %s not appeared on the web page" % (locator, locatorType))
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
            self.log.warn("Element %s  %s not disappeared from the web page" % (locator, locatorType))
            print_stack()

    def waitForElementToApear(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to Appear")
            wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            wait.until(EC.visibility_of_element_located((byType, locator)))
            self.log.info("Element %s  %s APPEARED on the web page" % (locator, locatorType))
        except:
            self.log.warn("Element %s  %s NOT APPEARED on the web page" % (locator, locatorType))
            print_stack()

    def switch_to_iframe(self, locatorType="id", locator=""):
        iframe_element = self.getElement(locator, locatorType)
        try:
            self.driver.switch_to.frame(iframe_element)
        except:
            self.log.warn("Cold not switch to iframe. locator: %s locator type: %s" % (locator, locatorType))
            print_stack()


    def execute_js_search(self, elem):
        elem = self.getElement(elem)
        my = 'name=selenium* and status=rebootinprogress'
        self.driver.execute_script("document.getElementById('SearchPanelView_searchStringInput').value=''")
        self.driver.execute_script("document.getElementById('SearchPanelView_searchStringInput').value='name=*L1* and status=rebootinprogress'")
        self.driver.execute_script("document.getElementById('SearchPanelView_searchButton').click()")
        self.log.info('Attempted to Executed JS')

    def scroll_down_till_element_in_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);",element)
        var = "//li/a[contains(text(), 'L3_nested_2')]"


    def write_delta_to_csv(self, test_function_name, delta):
        fileName = test_function_name + '.' + str(round(time.time() * 1000)) + '.csv'
        timeMeasureDir = '../time_measurements/'
        relativeFileName = timeMeasureDir + fileName.replace(" ", "")
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, timeMeasureDir)

        try:
            if not os.path.exists((destinationDirectory)):
                os.makedirs(destinationDirectory)

            with open(destinationFile, 'w') as full_path:
                full_path.write(str(delta))

            self.log.info('Time measure saved to directory: ' + destinationFile)
        except:
            self.log.error('### Exception Occured')
            print_stack()


    def start_timer(self):
        self.start_time = time.time()


    def stop_timer(self):
        self.end_time = time.time()
        delta = self.end_time - self.start_time
        return round(delta, 2)
