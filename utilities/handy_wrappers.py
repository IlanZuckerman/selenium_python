import inspect, time, os
from selenium.webdriver.common.by import By


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

    def write_delta_to_csv(self, suit_run_path, file_name, delta):
        with open(os.path.join(suit_run_path, file_name), 'w') as full_path:
            full_path.write(str(delta))
        print('wrote to ' + str(full_path))

    def measure_time(self, locator, bytype, start_time, timeout, suit_run_path):
        exit_condition = False
        while not exit_condition:
            exit_condition = self.isElementPresent(locator, bytype)

            print('Measuring time for locator: %s type: %s' % (locator, bytype))
            time.sleep(1)
            if (time.time() - start_time) > timeout:
                self.fail('It took more than %s seconds for element to appear: %s %s' % (timeout, locator, bytype))

        delta = time.time() - start_time
        self.write_delta_to_csv(suit_run_path, inspect.stack()[0][3], delta)
        print('It took %s seconds for element to appear: %s %s' % (delta, locator, bytype))
