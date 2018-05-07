from selenium.webdriver import ActionChains

from base.basepage import BasePage
from utilities.util import Util
import utilities.custom_logger as cl
import logging, time

class VmsPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.util = Util()

    # locators
    _compute = 'id-compute'
    _compute_vms = 'MenuView_vmsAnchor'
    _compute_hosts = 'MenuView_hostsAnchor'

    _new_vm_btn = 'ActionPanelView_NewVm'
    _new_host_btn = 'ActionPanelView_New'
    _management_dropdown_btn = 'ActionPanelView_Management'
    _management_dropdown_maintenance = "//div[@id='ActionPanelView_Management']//a[ contains(text(),'Maintenance') ]"
    _maintenance_dialog_ok_btn = 'HostMaintenanceConfirmationPopupView_OnMaintenance'
    _template_dropDown = "//div[@id='VmPopupWidget_templateWithVersion']/div/input"
    _cluster_dropDown = "//div[@id='VmPopupWidget_dataCenterWithCluster']//button"
    _vm_name_lbl = 'VmPopupWidget_name'
    _advanced_options_btn = 'VmPopupView_OnAdvanced'
    _resource_allocation_sideBar = "//div[@id='VmPopupWidget']//ul[@class='list-group']/li[8]"
    _thinDisk_radio = 'VmPopupWidget_provisioningThin'
    _ok_btn = 'VmPopupView_OnSave'
    _search_lbl = 'SearchPanelView_searchStringInput'
    _search_btn = 'SearchPanelView_searchButton'
    _new_vm_dialog = "class='popup-content ui-draggable'"
    _reboot_vm_btn = 'ActionPanelView_Reboot'
    _reboot_confirmation_btn = 'DefaultConfirmationPopupView_OnReboot'
    _clear_search_btn = "//div//button[@data-tooltip-content='Clear Search']"
    _run_vm_btn = "//div[@id='ActionPanelView_Run']/button[1]"

    # new hosts dialog
    _host_cluster_dropDown_btn = "//div[@id='HostPopupView_cluster']//button"
    _host_cluster_dropDown_menu = "//div[@id='HostPopupView_cluster']//ul[starts-with(@class, 'dropdown-menu')]"  # for scrolling
    _name_lbl = 'HostPopupView_name'
    _host_name_lbl = 'HostPopupView_host'  # for IP
    _password = 'HostPopupView_userPassword'
    _ok_false_btn = 'HostPopupView_OnSaveFalse'
    _power_management_ok_btn = 'DefaultConfirmationPopupView_OnSaveInternalNotFromApprove'

    # table elements
    _table_first_column = '//table//tbody/tr[{0}]/td[1]'  # used for clicking the row. formatted to use it in multiple rows
    _vm_name_field = "//table//tbody/tr[1]//td[3]//a[contains(text(),'{0}')]"  # {0} used for inserting vm name
    _no_items_to_display = "//tbody//div[text()='No items to display']"

    # dashboard iframe
    _dashboard_iframe = "//div//iframe"
    _elem_with_virtualResources_text = "//div[contains(text(),'Virtual resources')]"
    _elem_with_lastUpdated_text = "//b[contains(text(),'Last Updated')]"

    def hover_over_compute(self):
        element_to_hover = self.getElement(self._compute)
        ActionChains(self.driver).move_to_element(element_to_hover).perform()
        time.sleep(2)
        self.util.sleep(1, 'Hover over compute to work')

    def click_new(self):
        self.elementClick(self._new_vm_btn)

    def choose_template_from_dropdown(self, template_name):
        self.util.sleep(4, 'Create vm Dialog settle down')
        tmp = self.waitForElement(self._template_dropDown, 'xpath')
        self.elementClick(self._template_dropDown, 'xpath')
        self.elementClick("//td[contains(text(), '%s')]" % template_name, 'xpath')

    def enter_vm_name(self):
        self.name = 'vm_selenium' + str(round(time.time() * 1000))
        self.sendKeys(self.name, self._vm_name_lbl)
        return self.name

    def enter_name_for_new_host(self):
        self.name = 'host_selenium' + str(round(time.time() * 1000))
        self.sendKeys(self.name, self._name_lbl)
        return self.name

    def select_thinDisk(self):
        self.waitForElement(self._advanced_options_btn)

        advanced_btn_text = self.getElement(self._advanced_options_btn).text
        if 'Show' in advanced_btn_text:
            self.elementClick(self._advanced_options_btn)

        self.elementClick(self._resource_allocation_sideBar, 'xpath')
        self.waitForElement(self._thinDisk_radio)
        self.elementClick(self._thinDisk_radio)

    def validate_vm_status(self, status):
        # element = self.waitForElement("//tbody//div[contains(text(),'%s')]" % status, 'xpath', timeout=60)
        element = self.waitForElement("//tbody//div[(text()='%s')]" % status, 'xpath', timeout=120)
        return element is not None

    def validate_vm_name(self, vm_name):
        elem = self.waitForElement(self._vm_name_field.format(vm_name), locatorType='xpath', timeout=180)
        return elem is not None

    def search_for_selenium_vms(self, search_query, pause=3):
        self.waitForElementToDissapear(self._new_vm_dialog)
        self.waitForElementToApear(self._search_lbl)
        search_query = 'name=' + search_query
        self.sendKeys(data=search_query, locator=self._search_lbl)
        self.util.sleep(pause, 'Flickering when searching')
        self.elementClick(self._search_btn)
        self.util.sleep(pause, 'Search results settling down')

    def navigate_to_vms_page(self):
        self.hover_over_compute()
        self.elementClick(self._compute_vms)

    def navigate_to_hosts_page(self):
        self.hover_over_compute()
        self.elementClick(self._compute_hosts)

    def choose_cluster_from_dropdown(self, cluster_name):
        tmp = self.waitForElement(self._cluster_dropDown, 'xpath')
        self.elementClick(self._cluster_dropDown, 'xpath')
        self.elementClick("//li/a[contains(text(), '%s')]" % cluster_name, 'xpath')


    def create_new_vm_from_template(self, template_name, cluster_name):
        self.hover_over_compute()
        self.elementClick(self._compute_vms)
        self.elementClick(self._new_vm_btn)
        # self.util.sleep(3, 'Create vm Dialog settle down')
        self.choose_cluster_from_dropdown(cluster_name)
        self.choose_template_from_dropdown(template_name)

        vm_name = self.enter_vm_name()
        self.select_thinDisk()
        self.elementClick(self._ok_btn)
        self.waitForElementToDissapear(self._new_vm_dialog, 'xpath')
        return vm_name


    def create_new_host_with_ip(self, password, cluster, ip='172.16.12.223'):
        self.hover_over_compute()
        self.elementClick(self._compute_hosts)
        self.waitForElement(self._new_host_btn)
        time.sleep(1)
        self.elementClick(self._new_host_btn)
        tmp = self.waitForElement(self._host_cluster_dropDown_btn, 'xpath')
        self.elementClick(self._host_cluster_dropDown_btn, 'xpath')
        time.sleep(1)

        # drop_down_to_scroll = self.getElement(self._host_cluster_dropDown_menu, 'xpath')
        elem_to_scroll_to = self.getElement("//li/a[contains(text(), '%s')]" % cluster, 'xpath')
        self.scroll_down_till_element_in_view(elem_to_scroll_to)
        self.elementClick("//li/a[contains(text(), 'L3')]//parent::*",'xpath')
        name = self.enter_name_for_new_host()
        self.sendKeys(ip, self._host_name_lbl)
        self.sendKeys(password, self._password)
        self.elementClick(self._ok_false_btn)
        self.elementClick(self._power_management_ok_btn)
        return name

    def get_amount_of_rows_in_table(self, expected_rows_mnt):
        return self.verifyAmountOfRowsInTable(expected_rows_mnt)


    def is_iframe_rendered(self):
        self.waitForElementToApear(locator=self._dashboard_iframe, locatorType='xpath')
        self.switch_to_iframe(locator=self._dashboard_iframe, locatorType='xpath')
        elems_with_virtualElements_text = self.getElements(self._elem_with_virtualResources_text, 'xpath')
        time.sleep(0.2)
        elem_with_lastUpdated_text = self.getElement(self._elem_with_lastUpdated_text, 'xpath')
        elems_with_virtualElements_text.append(elem_with_lastUpdated_text)
        result = self.are_all_elems_displayed(elems_with_virtualElements_text)
        self.driver.switch_to_default_content()
        return result


    def are_all_elems_displayed(self, elems_list):
        for elem in elems_list:
            if not self.isElementDisplayed(element=elem):
                return False
        return True

    def select_nth_row_of_the_table(self, row_number):
        # first row is 1. repeating because sometimes selection fails.
        for i in range(2):
            self.elementClick(locator=self._table_first_column.format(row_number), locatorType='xpath')

    def select_multiple_rows_from_table(self, untill_row, from_row=1):
        # from_row=1 meaning first row will be selected
        self.select_nth_row_of_the_table(row_number=from_row)
        for i in range(2):
            self.elementClickShift(locator=self._table_first_column.format(untill_row), locatorType='xpath')

    def reboot_vms(self):
        self.waitForElement(self._reboot_vm_btn)
        self.elementClick(self._reboot_vm_btn)
        self.elementClick(self._reboot_confirmation_btn)

    def clear_search_field(self):
        self.elementClick(self._clear_search_btn, locatorType='xpath')

    def search_vms_in_reboot_with_js(self):
        self.driver.execute_script("document.getElementById('SearchPanelView_searchStringInput').value=''")
        self.driver.execute_script("document.getElementById('SearchPanelView_searchStringInput').value='name=*L1* and status=rebootinprogress'")
        self.driver.execute_script("document.getElementById('SearchPanelView_searchButton').click()")
        self.util.sleep(sec=1, info='Waiting 1 sec after search_vms_in_reboot_with_js ')
        self.log.info('Attempted to Executed JS search_vms_in_reboot_with_js')

    def wait_till_results_table_starts_painting(self):
        self.waitForElement(self._table_first_column.format('1'), locatorType='xpath', timeout=30)
        print('started painting')

    def wait_till_NoItemsToDisplay_appears(self):
        return self.waitForElement(self._no_items_to_display, locatorType='xpath', timeout=120)

    def click_run_vm_btn(self):
        self.waitForElement(self._run_vm_btn, 'xpath')
        self.elementClick(self._run_vm_btn, 'xpath')