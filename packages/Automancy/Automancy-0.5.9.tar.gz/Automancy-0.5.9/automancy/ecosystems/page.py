from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as wait
from selenium.webdriver.support.ui import WebDriverWait

from ..core import Browser, Model


class Page(Model):
    """
    The Elemental meant to contain data about and controls for an entire page that is being tested
    Further Elementals that are created from here are child elements derived from this objects content
    Intended to manage the state of the page and webdriver related to the tests that are being run.
    """
    def __init__(self, url='', browser=None):
        Model.__init__(self)
        self.browser = self.browser = browser if browser else Browser.find_driver()
        self.element = None
        self.url = url
        self.locator = ''

    def __call__(self):
        self.visit()

    def switch_to_parent(self):
        """ Switches back to the default page HTML after having switched to an iframe for example """
        self.browser.switch_to.parent_frame()

    def switch_to_iframe(self, xpath_string='//iframe'):
        """
        Switch to a target iframe after waiting for the presence of the element.

        If there is content within an iframe with in the main html body,
        that iframe must be switched to using this method before testing can continue.

        Args:
            xpath_string (str): Optional, the xpath string used to search for the element that we're going to switch to

        Returns:
            None

        """
        element = WebDriverWait(self.browser, 30).until(wait.presence_of_element_located((By.XPATH, xpath_string)))

        if element:
            self.browser.switch_to.frame(element)

    def refresh(self):
        """
        Refreshes the contents of the entire page WebElement allowing other elements to update their state
        """
        self.element = WebDriverWait(self.browser, 30).until(wait.presence_of_element_located((By.XPATH, self.locator)))

    def current_url(self):
        """
        Wrapper for driver.current_url
        :return: The current url know by the driver
        :rtype: str
        """
        return self.browser.current_url

    def visit(self):
        """
        Wrapper for driver.get(url)
        :return: None
        """
        self.browser.get(self.url)

    def wait_for_visibility(self, selector):
        """
        Causes the operation to wait for the visibility of an element before proceeding
        :param selector: The string that represents the target for query
        :type selector: str
        """
        return WebDriverWait(self.browser, 10).until(wait.visibility_of_element_located((By.XPATH, selector)))
