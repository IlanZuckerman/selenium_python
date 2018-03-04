from selenium.webdriver import ActionChains

from base.selenium_driver import SeleniumDriver
import utilities.custom_logger as cl
import logging, time

class VmsPage(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    _compute = 'id-compute'
    _compute_vms = 'MenuView_vmsAnchor'

    _new_btn = 'ActionPanelView_NewVm'
    _template_dropDown = "//div[@id='VmPopupWidget_templateWithVersion']/div/input"
    _vm_name_lbl = 'VmPopupWidget_name'
    _advanced_options_btn = 'VmPopupView_OnAdvanced'
    _resource_allocation_sideBar = "//div[@id='VmPopupWidget']//ul[@class='list-group']/li[8]"
    _thinDisk_radio = 'VmPopupWidget_provisioningThin'
    _ok_btn = 'VmPopupView_OnSave'
    _search_lbl = 'SearchPanelView_searchStringInput'
    _search_btn = 'SearchPanelView_searchButton'

    def hover_over_compute(self):
        element_to_hover = self.getElement(self._compute)
        ActionChains(self.driver).move_to_element(element_to_hover).perform()
        time.sleep(2)

    def click_new_vm(self):
        self.elementClick(self._new_btn)

    def choose_template_from_dropdown(self, template_name):
        tmp = self.waitForElement(self._template_dropDown, 'xpath')
        self.elementClick(self._template_dropDown, 'xpath')
        self.elementClick("//*[contains(text(), '%s')]" % template_name, 'xpath')

    def enter_vm_name(self):
        self.name = 'selenium' + str(round(time.time() * 1000))
        self.sendKeys(self.name, self._vm_name_lbl)

    def select_thinDisk(self):
        self.elementClick(self._advanced_options_btn)
        self.elementClick(self._resource_allocation_sideBar, 'xpath')
        time.sleep(3)
        self.elementClick(self._thinDisk_radio)

    def validate_vm_created(self):
        element = self.waitForElement("//tbody//a[contains(text(),'%s')]" % self.name, 'xpath', timeout=30)
        return element is not None

    def search_for_selenium_vms(self):
        # TODO: change this wait to something like "if visible on page"
        time.sleep(1)
        tmp = self.waitForElement(self._search_btn)
        self.sendKeys('name=selenium*', self._search_lbl)
        self.elementClick(self._search_btn)


    def create_new_vm_from_template(self, template_name):
        self.hover_over_compute()
        self.elementClick(self._compute_vms)
        self.click_new_vm()
        self.choose_template_from_dropdown(template_name)
        self.enter_vm_name()
        self.select_thinDisk()
        self.elementClick(self._ok_btn)

