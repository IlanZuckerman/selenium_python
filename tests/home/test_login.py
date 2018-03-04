# pip freeze > requirements.txt
# pip install -r requirements.txt

import time, os, datetime, logging, unittest, pytest
from pages.home.login_page import LoginPage
from pages.vms.vms_page import VmsPage
from utilities.teststatus import TestStatus

@pytest.mark.usefixtures('oneTimeSetUp', 'setUp')
class TestLogin(unittest.TestCase):

    # log = cl.customLogger(logging.DEBUG)

    # @classmethod
    # def setUpClass(cls):
    #     """
    #     Run only once per execution
    #     Create directory tree in /tmp per each test suit execution
    #     """
    #     t = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    #     cls.suit_run_path = os.path.join('/tmp/RHV_4_1_Scale_Up/', t)
    #     # log.info ('going to create file: ' + cls.suit_run_path)
    #     os.makedirs(cls.suit_run_path)


    # def setUp(self):
    #     """
    #     Run once before each test case
    #     """
    #     self.lp = LoginPage(self.driver)

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.vp = VmsPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=2)
    def test_valid_login(self):
        # start_time = self.login()
        # self.hw.measure_time('id-compute', 'id', start_time, 15, self.suit_run_path)
        # self.assertIn('Red Hat Virtualization Manager Web Administration', self.driver.title, 'Title is not as expected')

        self.lp.login('admin', 'qum5net')
        result1 = self.lp.verifyTitle()
        self.ts.mark(result1, 'Title Verified')
        result2 = self.lp.verifyLoginSuccesfull()
        self.ts.markFinal('test_valid_login', result2, 'Login successful')
        time.sleep(3)

    @pytest.mark.run(order=1)
    def test_invalid_login(self):
        self.lp.clickWelcomeAdminField()
        self.lp.login()
        result = self.lp.verifyLoginFailed()
        self.ts.markFinal('test_invalid_login', result, 'Invalid login went good')
        # assert result == True
        time.sleep(3)

    @pytest.mark.run(order=3)
    def test_create_vm_from_template(self):
        self.vp.create_new_vm_from_template('1_HDD_Thin')
        self.vp.search_for_selenium_vms()
        result = self.vp.validate_vm_created()
        self.ts.markFinal('test_create_vm_from_template', result, 'vm created successfully')
        # assert result == True

    #     element_to_hover_over = self.driver.find_element_by_id("id-compute")
    #     hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
    #     hover.perform()
    #     time.sleep(3)
    #     self.driver.find_element_by_id("MenuView_vmsAnchor").click()
    #     # time.sleep(WAIT_BETWEEN_ACTIONS)
    #     self.driver.find_element_by_id('ActionPanelView_NewVm').click()
    #     time.sleep(3)
    #     self.driver.find_element_by_xpath("//*[@id='VmPopupWidget_templateWithVersion']/div/input").click()
    #     time.sleep(3)
    #     self.driver.find_element_by_xpath("//*[contains(text(), 'small_vm')]").click()
    #     time.sleep(3)
    #     self.driver.find_element_by_id('VmPopupWidget_name').send_keys('0selenium_vm_%s' %(random.randint(1, 99)))
    #     time.sleep(3)
    #     self.driver.find_element_by_id('VmPopupView_OnSave').click()
    #
    #     start = time.time()
    #     time.sleep(3)
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


    # def tearDown(inst):
    #     # close the browser window
    #     inst.driver.quit()
