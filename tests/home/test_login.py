# pip freeze > requirements.txt
# pip install -r requirements.txt
import time, unittest, pytest, re, inspect
from pages.home.login_page import LoginPage
from pages.vms.vms_page import VmsPage
from utilities.teststatus import TestStatus

@pytest.mark.usefixtures('oneTimeSetUp', 'setUp')
class TestLogin(unittest.TestCase):
    vm_name = ''
    ip_172 = []
    host_name = ''

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.vp = VmsPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.run(order=1)
    def test_invalid_login(self):
        self.lp.clickWelcomeAdminField()
        self.lp.login()
        result = self.lp.verifyLoginFailed()
        self.ts.markFinal('test_invalid_login', result, 'Invalid login went good')
        # assert result == True
        time.sleep(3)

    @pytest.mark.run(order=2)
    def test_valid_login(self):

        self.lp.start_timer()
        self.lp.login('admin', 'qum5net')
        result2 = self.lp.verifyLoginSuccesfull()
        result1 = self.lp.verifyTitle()
        delta = self.lp.stop_timer()
        self.lp.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=delta)
        self.ts.mark(result2, 'Title Verified')
        self.ts.markFinal('test_valid_login', result1, 'Login successful')
        time.sleep(3)


    @pytest.mark.run(order=3)
    def test_create_L1vm_from_template(self):
        self.__class__.vm_name = self.vp.create_new_vm_from_template('L1_vm_08-02', cluster_name='L1_vms')
        self.ts.start_timer()
        # waiting for popup to disappear
        self.ts.waitForElementToDissapear('class="popup-content ui-draggable"', 'xpath')

        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Down')
        time.sleep(2)

        # this is for dealing with double flicker thing
        rows_amount = len(self.lp.getElements('//tbody/tr', 'xpath'))
        while rows_amount > 1:
            self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Down')
            time.sleep(2)
            rows_amount = len(self.lp.getElements('//tbody/tr', 'xpath'))

        first_row_painting = self.lp.waitForElement("//table//tbody/tr[1]/td[2]", locatorType='xpath', timeout=180)
        self.ts.markFinal('test_create_vm_from_template', first_row_painting, 'vm created successfully')
        delta = self.ts.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=delta)


    @pytest.mark.run(order=4)
    def test_start_previosly_created_L1_vm(self):
        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Down')
        time.sleep(3)

        # starting vm
        tmp = self.lp.waitForElement("//div[@id='ActionPanelView_Run']/button[1]", 'xpath')
        self.lp.elementClick("//div[@id='ActionPanelView_Run']/button[1]", 'xpath')
        self.vp.start_timer()
        time.sleep(2)

        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Up')
        time.sleep(2)
        first_row_painting = self.lp.waitForElement("//table//tbody/tr[1]/td[2]", locatorType='xpath', timeout=180)
        self.ts.markFinal('test_start_previosly_created_vm', first_row_painting, 'vm started successfully')
        delta = self.vp.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=delta)

    @pytest.mark.run(order=5)
    def test_reboot_bulk_of_20_L1_vms(self):
        self.vp.navigate_to_vms_page()

        self.vp.search_for_selenium_vms('*L1* and status=up')
        time.sleep(5)
        rows_amount = len(self.lp.getElements('//tr', 'xpath'))
        if rows_amount > 2:
            for i in range(1, 21):
                self.lp.elementClickShift('//table//tbody/tr[%s]/td[1]' % (i), 'xpath')
        # starting vm
        tmp = self.vp.waitForElement('ActionPanelView_Reboot')
        self.vp.elementClick("ActionPanelView_Reboot")
        self.vp.elementClick('DefaultConfirmationPopupView_OnReboot')
        self.vp.start_timer()

        self.vp.elementClick("//div//button[@data-tooltip-content='Clear Search']", 'xpath')
        self.vp.execute_js_search('SearchPanelView_searchStringInput')
        time.sleep(3)

        first_row_painting = self.lp.waitForElement("//table//tbody/tr[1]/td[2]", locatorType='xpath', timeout=30)
        print('started painting')
        # wait till there is nothing to show
        no_rows_result = self.lp.waitForElement("//tbody//div[text()='No items to display']", locatorType='xpath', timeout=60)
        self.ts.markFinal('test_reboot_10_vm', no_rows_result, 'vms rebooted successfully')
        delta = self.vp.stop_timer()
        self.vp.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=delta)

    @pytest.mark.run(order=6)
    def test_create_L2vm_from_template(self):
        self.__class__.vm_name = self.vp.create_new_vm_from_template(template_name='L2_vm_13-02', cluster_name='L2_real')
        self.ts.start_timer()
        # waiting for popup to disappear
        self.ts.waitForElementToDissapear('class="popup-content ui-draggable"', 'xpath')

        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Down')
        time.sleep(2)
        first_row_painting = self.lp.waitForElement("//table//tbody/tr[1]/td[2]", locatorType='xpath', timeout=300)

        self.ts.markFinal('test_create_vm_from_template', first_row_painting, 'vm created successfully')
        delta = self.ts.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=delta)

    @pytest.mark.run(order=7)
    def test_start_previosly_created_L2_vm(self):
        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Down')
        self.vp.start_timer()
        time.sleep(3)

        # starting vm
        tmp = self.lp.waitForElement("//div[@id='ActionPanelView_Run']/button[1]", 'xpath')
        self.lp.elementClick("//div[@id='ActionPanelView_Run']/button[1]", 'xpath')
        time.sleep(2)

        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Up')
        first_row_painting = self.lp.waitForElement("//table//tbody/tr[1]/td[2]", locatorType='xpath', timeout=300)

        for i in range(1, 30):
            ip_elem = self.vp.getElement('//table//tbody/tr[1]/td[6]/div/div', 'xpath')
            if ip_elem is not None:
                try:
                    dirty_ip = ip_elem.text
                    self.__class__.ip_172 = re.findall(r'172.\d+\.\d+\.\d+', dirty_ip)
                    if self.__class__.ip_172:
                        break
                except:
                    pass
            time.sleep(1)

        if len(self.__class__.ip_172) == 0:
            self.__class__.ip_172 = None

        self.ts.mark(self.__class__.ip_172, 'The started L2 vm didnt get 172 ip. Extracted ip: ' + str(self.__class__.ip_172))
        self.ts.markFinal('test_start_previosly_created_vm', first_row_painting, 'vm started successfully'
                          + 'Extracted ip: ' + str(self.__class__.ip_172))
        delta = self.vp.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=delta)

    @pytest.mark.run(order=8)
    def test_create_nested_host_and_check_status(self):
        self.__class__.host_name = self.vp.create_new_host_with_ip(ip=self.__class__.ip_172, password='redhat', cluster='L3_nested_2')
        self.vp.start_timer()

        self.vp.navigate_to_hosts_page()
        # tmp_hostname = 'host_selenium1520506322330'
        self.vp.search_for_selenium_vms(self.__class__.host_name + ' and status=Up')
        first_row_painting = self.lp.waitForElement("//table//tbody/tr[1]//td[3]//a[contains(text(),'%s')]"
                                                    % self.__class__.host_name, locatorType='xpath', timeout=180)
        self.ts.markFinal('test_status_of_nested_host', first_row_painting,
                          'Nested host created successfully ' + self.__class__.host_name)
        delta = self.vp.stop_timer()
        self.vp.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=delta)

    @pytest.mark.run(order=9)
    def test_putting_bulk_of_nested_hosts_to_maintenance(self):
        self.vp.navigate_to_hosts_page()
        self.vp.search_for_selenium_vms('*selenium* and status=Up')
        # TODO: think how to handle this sleep. it is because search results flickers couple of times
        time.sleep(10)
        rows_amount = len(self.lp.getElements('//tr', 'xpath'))
        if rows_amount > 2:
            for i in range(1, rows_amount):
                self.lp.elementClickShift('//table//tbody/tr[%s]/td[1]' % (i), 'xpath')

        self.vp.elementClick(self.vp._management_dropdown_btn)
        self.vp.elementClick(self.vp._management_dropdown_maintenance, 'xpath')
        self.vp.elementClick(self.vp._maintenance_dialog_ok_btn)
        # TODO: add validations and time measurements
