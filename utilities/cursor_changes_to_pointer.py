class CursorChangesFromWaiting():
    """Helper class for waiting until the cursor changes back to normal)"""
    def __init__(self, browser):
        self.browser = browser

    def __call__(self, ignored):
        """This will be called every 500ms by Selenium until it returns true (or we time out)"""
        cursor = self.browser.find_element_by_xpath("//button[@type='submit']").value_of_css_property("cursor")
        return cursor == "bla"