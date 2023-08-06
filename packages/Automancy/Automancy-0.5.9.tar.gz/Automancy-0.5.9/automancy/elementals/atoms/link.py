""" ./atoms/link.py"""
import time

from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, ElementNotInteractableException

from automancy.core import Elemental, WaitForPageLoad


class Link(Elemental):
    """ Atomic Elemental for link web elements """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Notes:
            Link objects utilize the WaitForPageLoad class when clicking the element.
            The design reason is outlined in the docstring for the overridden .click()
            method below and in the WaitForPageLoad class docstring.

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)

    def click(self) -> None:
        """
        Override for the base class' click method.

        The reason for this specific override is because links generally take the user
        to a new page rather than something like a button which may simply submit a form.

        We want to wait for the new page to load after clicking the link which is vital
        for tests to continue and we don't want to do the work of explicitly telling
        the tests when and where to wait.

        This override allows us to implicitly do the work without the test author ever
        knowing.
        """
        with WaitForPageLoad(self.browser):
            try:
                if not self.visible:
                    self.scroll_to()

                self.element().click()
            except ElementNotVisibleException:
                time.sleep(3)
                self.element().click()
            except WebDriverException as error:
                if isinstance(error, ElementNotInteractableException):
                    self.browser.execute_script('arguments[0].click()', self.element())
