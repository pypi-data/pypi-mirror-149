from .version import VERSION
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from robot.api import logger
from .util import Util

class WaitHelper(Util):

    def __init__(self):
        pass
    
    @keyword("Wait Until Element Is Visible With Retry")
    def wait_until_element_is_visible_with_retry(self, locator, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Element Is Visible", locator)
    
    @keyword("Wait Until Element Is Not Visible With Retry")
    def wait_until_element_is_not_visible_with_retry(self, locator, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Element Is Not Visible", locator)
    
    @keyword("Wait Until Page Contains With Retry")
    def wait_until_page_contains_with_retry(self, text, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Page Contains", text)
    
    @keyword("Wait Until Page Does Not Contain With Retry")
    def wait_until_page_does_not_contain_with_retry(self, text, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Page Does Not Contain", text)
    
    @keyword("Wait Until Page Contains Element With Retry")
    def wait_until_page_contains_element_with_retry(self, locator, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Page Contains Element", locator)
    
    @keyword("Wait Until Page Does Not Contain Element With Retry")
    def wait_until_page_does_not_contain_element_with_retry(self, locator, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Page Does Not Contain Element", locator)
    
    @keyword("Wait For WebElement")
    def wait_for_webelement(self, locator):
        """
        Wait for `locator` present in webpage then scroll to element
        """
        self.sellib = BuiltIn().get_library_instance('SeleniumLibrary')
        try:
            Util.wait_for_element(self, self.sellib, locator)
        except Exception as e:
            Util.log_failure(self, self.sellib, e)

    @keyword("Wait For WebElement Disappear")
    def wait_for_webelement_disappear(self, locator):
        """
        Wait for `locator` not present in webpage
        """
        self.sellib = BuiltIn().get_library_instance('SeleniumLibrary')
        try:
            Util.wait_for_element_not_present(self, self.sellib, locator)
        except Exception as e:
            Util.log_failure(self, self.sellib, e) 

    @keyword("Wait For WebElement With Retry")
    def wait_for_webelement_with_retry(self, locator, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumHelperLibrary.Wait For WebElement", locator)
    
    @keyword("Wait For WebElement Disappear With Retry")
    def wait_for_webelement_disappear_with_retry(self, locator, retry="3x", retry_interval="2s"):
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumHelperLibrary.Wait For WebElement Disappear", locator)

    @keyword("Wait Until DOM Loaded")
    def wait_until_dom_loaded(self):
        """
        Wait until dom loaded in web page
        """
        self.sellib = BuiltIn().get_library_instance('SeleniumLibrary')
        try:
            self.sellib.wait_for_condition('return window.document.readyState === "complete"')
        except Exception as e:
            Util.log_failure(self, self.sellib, e)
    
    @keyword("Wait Until Element Contains With Retry")
    def wait_until_element_contains_with_retry(self, locator, value, retry="3x", retry_interval="2s"):
        self.sellib = BuiltIn().get_library_instance('SeleniumLibrary')
        Util.wait_for_element(self, self.sellib, locator)
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Element Contains", locator, value)
    
    @keyword("Wait Until Element Does Not Contain With Retry")
    def wait_until_element_does_not_contain_with_retry(self, locator, value, retry="3x", retry_interval="2s"):
        self.sellib = BuiltIn().get_library_instance('SeleniumLibrary')
        Util.wait_for_element(self, self.sellib, locator)
        BuiltIn().wait_until_keyword_succeeds(retry, retry_interval, "SeleniumLibrary.Wait Until Element Does Not Contain", locator, value)