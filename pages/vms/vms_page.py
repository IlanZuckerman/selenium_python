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
        self.elementClick("//*[contains(text(), '%s')]" % template_name, 'xpath')

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

    def search_for_selenium_vms(self, vm_name):
        # TODO: change this wait to something like "if visible on page"
        # time.sleep(3)

        elem = self.waitForElementToApear(self._search_lbl, 'xpath')
        search_query = 'name=' + vm_name
        self.sendKeys(search_query, self._search_lbl)
        self.util.sleep(3, 'Flickering when searching')
        self.elementClick(self._search_btn)
        self.util.sleep(3, 'Search results settling down')

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
        self.scroll_down(elem_to_scroll_to)
        self.elementClick("//li/a[contains(text(), 'L3')]//parent::*",'xpath')
        name = self.enter_name_for_new_host()
        self.sendKeys(ip, self._host_name_lbl)
        self.sendKeys(password, self._password)
        self.elementClick(self._ok_false_btn)
        self.elementClick(self._power_management_ok_btn)
        return name

    def get_amount_of_rows_in_table(self, expected_rows_mnt):
        return self.verifyAmountOfRowsInTable(expected_rows_mnt)
