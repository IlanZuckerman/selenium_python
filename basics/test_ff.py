# pip freeze > requirements.txt
# pip install -r requirements.txt
import inspect
import random

from selenium import webdriver
import time, os, datetime, logging, unittest

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from utilities.handy_wrappers import HandyWrappers
import utilities.custom_logger as cl
from pages.home.login_page import LoginPage

IMPLICIT_WAIT = 5


class TestFF(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Run only once per execution
        Create directory tree in /tmp per each test suit execution
        """
        log = cl.customLogger(logging.DEBUG)
        t = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        cls.suit_run_path = os.path.join('/tmp/RHV_4_1_Scale_Up/', t)
        log.info ('going to create file: ' + cls.suit_run_path)
        os.makedirs(cls.suit_run_path)


    def setUp(self):
        """
        Run once before each test case
        """
        self.profile = webdriver.FirefoxProfile()
        self.profile.accept_untrusted_certs = True
        self.driver = webdriver.Firefox(firefox_profile=self.profile)
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        # inst.driver.maximize_window()
        self.driver.get('https://vega09.qa.lab.tlv.redhat.com/ovirt-engine/')
        # self.hw = HandyWrappers(self.driver)


    # def login(self):
    #     welcome_webadmin_btn = self.hw.getElement('WelcomePage_webadmin')
    #     welcome_webadmin_btn.click()
    #     username_lbl = self.hw.getElement('username')
    #     password_lbl = self.hw.getElement('password')
    #     login_btn = self.hw.getElement('//button[@type="submit"]', 'xpath')
    #     username_lbl.send_keys('admin')
    #     password_lbl.send_keys("qum5net")
    #     login_btn.click()
    #     return time.time()
        # time.sleep(5)


    def test_login(self):
        # start_time = self.login()
        # self.hw.measure_time('id-compute', 'id', start_time, 15, self.suit_run_path)
        # self.assertIn('Red Hat Virtualization Manager Web Administration', self.driver.title, 'Title is not as expected')

        lp = LoginPage(self.driver)
        lp.login('admin', 'qum5net')
        # time.sleep(3)
        self.assertIn('Red Hat Virtualization Manager Web Administration', self.driver.title,
                      'Title is not as expected')



    # def test_create_vm_from_template(self):
    #     lp = LoginPage(self.driver)
    #     lp.login('admin', 'qum5net')
    #     time.sleep(5)
    #     element_to_hover_over = self.driver.find_element_by_id("id-compute")
    #     hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
    #     hover.perform()
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.driver.find_element_by_id("MenuView_vmsAnchor").click()
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.driver.find_element_by_id('ActionPanelView_NewVm').click()
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.driver.find_element_by_xpath("//*[@id='VmPopupWidget_templateWithVersion']/div/input").click()
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.driver.find_element_by_xpath("//*[contains(text(), 'small_vm')]").click()
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.driver.find_element_by_id('VmPopupWidget_name').send_keys('0selenium_vm_%s' %(random.randint(1, 99)))
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.driver.find_element_by_id('VmPopupView_OnSave').click()
    #
    #     start = time.time()
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.assertFalse(self.is_element_present(By.XPATH, "//*[contains(text(), 'Error while executing action: ')]"), 'Error popup triggered')
    #
    #     exit_condition = False
    # # Loop while vm is still creating and measure time
    #     while exit_condition == False:
    #         first_row = self.driver.find_element_by_xpath("//div[@id='MainVirtualMachineView_table_content_col0_row0']")
    #         first_row_status = first_row.get_attribute('data-status')
    #         print('status: ' + first_row_status)
    #         exit_condition = (first_row_status == 'Down')
    #         time.sleep(1)
    #         if (time.time() - start) > 240: self.fail('It took more than 4min for vm to be created')
    #
    #     delta = time.time() - start
    #     print('it took %s seconds to create vm' %(delta))
    #     self.write_delta_to_csv(self.suit_run_path, inspect.stack()[0][3], delta)


    def tearDown(inst):
        # close the browser window
        inst.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)