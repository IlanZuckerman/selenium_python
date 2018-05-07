# pip freeze > requirements.txt
# pip install -r requirements.txt
import time, unittest, pytest, re, inspect
from pages.home.login_page import LoginPage
from pages.vms.vms_page import VmsPage
from utilities.teststatus import TestStatus
from ddt import ddt, data, unpack
from utilities.read_data import getCSVData
from utilities.write_to_exec_report import ReportWriter


@pytest.mark.usefixtures('oneTimeSetUp', 'setUp')  # names of fixtures we wanna use from conftest
@ddt
class TestLogin(unittest.TestCase):
    vm_name = ''
    ip_172 = []
    host_name = ''

    report_writer = ReportWriter()

    @pytest.fixture(autouse=True)  # autouse makes this fixture available for all methods in scope
    def classSetup(self, oneTimeSetUp, username, password):
        self.lp = LoginPage(self.driver)
        self.vp = VmsPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.username = username
        self.password = password
        self.delta = None
        self.test_function_name = None

        self.vm_name_for_reboot = '*L1*'
        self.template_for_L1_vms = 'L1_vm_08-02'
        self.cluster_for_L1_vms = 'L1_vms'

        self.template_for_L2_vms = 'L2_vm_13-02'
        self.cluster_for_L2_vms = 'L2_real'

        yield
        self.__class__.report_writer.exec_report_handler(delta=self.delta, test_function_name=self.test_function_name)


    @pytest.mark.run(order=1)
    def test_invalid_login(self):
        a = self.moshe
        self.test_function_name=inspect.stack()[0][3]
        self.lp.clickWelcomeAdminField()
        self.lp.login()
        result = self.lp.verifyLoginFailed()
        self.ts.markFinal('test_invalid_login', result, 'Invalid login went good')

    @pytest.mark.run(order=2)
    def test_login_dashboard_paint(self):
        self.test_function_name=inspect.stack()[0][3]
        self.lp.login(self.username, self.password)
        self.lp.start_timer()

        result = self.vp.is_iframe_rendered()
        self.ts.markFinal('test_login_dashboard_paint', result, 'Login successful and dashboard painted')

        self.delta = self.lp.stop_timer()
        self.lp.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=self.delta)

    @pytest.mark.run(order=3)
    @data(10, 50, 80, 100)
    # @data(*getCSVData('path_to_csv_file')) # to use data from csv
    def test_reboot_vms_in_bulk_of(self, bulk):
        self.test_function_name=inspect.stack()[0][3] + str(bulk)

        self.vp.navigate_to_vms_page()
        self.vp.search_for_selenium_vms(self.vm_name_for_reboot + ' and status=up')
        self.vp.select_multiple_rows_from_table(untill_row=bulk)
        self.vp.reboot_vms()
        self.vp.start_timer()
        self.vp.clear_search_field()

        # instead, we could use this: its just the JS is faster.
        #  self.vp.search_for_selenium_vms(self.vm_name_for_reboot + ' nd status=rebootinprogress',pause=0.3)
        self.vp.search_vms_in_reboot_with_js()
        self.vp.wait_till_results_table_starts_painting()
        # wait till there is nothing to show
        no_rows_result = self.vp.wait_till_NoItemsToDisplay_appears()

        self.ts.markFinal('test_reboot_bulk_vm', no_rows_result, 'vms rebooted successfully')
        self.delta = self.vp.stop_timer()
        self.vp.write_delta_to_csv(test_function_name=inspect.stack()[0][3] + str(bulk), delta=self.delta)

    @pytest.mark.run(order=4)
    def test_create_L1_vm_from_template(self):
        self.test_function_name=inspect.stack()[0][3]

        self.__class__.vm_name = self.vp.create_new_vm_from_template(
            template_name=self.template_for_L1_vms,
            cluster_name=self.cluster_for_L1_vms)
        self.ts.start_timer()

        self.vp.search_for_selenium_vms(search_query=self.__class__.vm_name + ' and status=Down')
        result = self.vp.validate_vm_name(vm_name=self.__class__.vm_name)

        self.ts.markFinal('test_create_vm_from_template', result, 'vm created successfully')
        self.delta = self.ts.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=self.delta)

    @pytest.mark.run(order=5)
    def test_start_previosly_created_L1_vm(self):
        self.test_function_name=inspect.stack()[0][3]

        self.vp.click_run_vm_btn()
        self.vp.start_timer()

        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Up')
        result = self.vp.validate_vm_name(vm_name=self.__class__.vm_name)

        self.ts.markFinal('test_start_previosly_created_vm', result, 'vm started successfully')
        self.delta = self.vp.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=self.delta)

    @pytest.mark.run(order=6)
    def test_create_L2_vm_from_template(self):
        self.test_function_name=inspect.stack()[0][3]

        self.__class__.vm_name = self.vp.create_new_vm_from_template(
            template_name=self.template_for_L2_vms,
            cluster_name=self.cluster_for_L2_vms)
        self.ts.start_timer()

        self.vp.search_for_selenium_vms(self.__class__.vm_name + ' and status=Down')
        result = self.vp.validate_vm_name(vm_name=self.__class__.vm_name)

        self.ts.markFinal('test_create_vm_from_template', result, 'vm created successfully')
        self.delta = self.ts.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=self.delta)

    @pytest.mark.run(order=7)
    def test_start_previosly_created_L2_vm(self):
        self.test_function_name=inspect.stack()[0][3]

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
        self.delta = self.vp.stop_timer()
        self.ts.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=self.delta)

    @pytest.mark.run(order=8)
    def test_create_nested_host_and_check_status(self):
        self.test_function_name=inspect.stack()[0][3]

        self.__class__.host_name = self.vp.create_new_host_with_ip(ip=self.__class__.ip_172, password='redhat', cluster='L3_nested_2')
        self.vp.start_timer()

        self.vp.navigate_to_hosts_page()
        # tmp_hostname = 'host_selenium1520506322330'
        self.vp.search_for_selenium_vms(self.__class__.host_name + ' and status=Up')
        first_row_painting = self.lp.waitForElement("//table//tbody/tr[1]//td[3]//a[contains(text(),'%s')]"
                                                    % self.__class__.host_name, locatorType='xpath', timeout=300)
        self.ts.markFinal('test_status_of_nested_host', first_row_painting,
                          'Nested host created successfully ' + self.__class__.host_name)
        self.delta = self.vp.stop_timer()
        self.vp.write_delta_to_csv(test_function_name=inspect.stack()[0][3], delta=self.delta)

    # @pytest.mark.run(order=3)
    # @data(100)
    # def test_putting_bulk_of_nested_hosts_to_maintenance(self, bulk):
    #     self.vp.navigate_to_hosts_page()
    #     self.vp.search_for_selenium_vms('*nested* and status=Up')
    #
    #     # select first row
    #     self.vp.elementClick('//table//tbody/tr[1]/td[1]', 'xpath')
    #     self.vp.elementClick('//table//tbody/tr[1]/td[1]', 'xpath')
    #     self.vp.elementClick('//table//tbody/tr[1]/td[1]', 'xpath')
    #
    #     # select last row
    #     last_row = self.vp.getElement('//table//tbody/tr[%s]/td[1]' % (int(bulk)), 'xpath')
    #     self.vp.elementClickShift(elem=last_row)
    #     self.vp.elementClickShift(elem=last_row)
    #     self.vp.elementClickShift(elem=last_row)
    #
    #     self.vp.elementClick(self.vp._management_dropdown_btn)
    #     self.vp.elementClick(self.vp._management_dropdown_maintenance, 'xpath')
    #     self.vp.elementClick(self.vp._maintenance_dialog_ok_btn)
    #
    #     self.vp.start_timer()
    #
    #     self.vp.search_for_selenium_vms('*nested* and status=preparingformaintenance')
    #
    #     result = self.vp.verifyAmountOfRowsInTable(expected_rows_amount=1, allowed_offset=0)  # 1 because there is row with 'no results'
    #     self.ts.markFinal(testName=inspect.stack()[0][3] + str(bulk), result=result,
    #                       resultMessage='Nested hosts put to Maintenance successful')
    #
    #     delta = self.vp.stop_timer() - 6  # compensating 6 seconds of waits in search_for_selenium_vms
    #     self.vp.write_delta_to_csv(test_function_name=inspect.stack()[0][3] + str(bulk), delta=delta)