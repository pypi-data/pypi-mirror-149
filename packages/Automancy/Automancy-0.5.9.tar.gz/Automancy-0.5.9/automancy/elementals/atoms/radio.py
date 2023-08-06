""" ./atoms/radio.py """
from automancy.core import Elemental


class Radio(Elemental):
    """ Atom Elemental for radio option DOM objects """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Represents a radio option selector DOM element, the kind of element
        used in a form where only one of a set of options can be selected at
        a time.

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)

    def is_selected(self):
        """
        Wrapper for the Selenium WebElement 'is_selected' method

        Returns:
            bool: True if currently selected, False if not.

        """
        return self.element().is_selected()

    def select(self):
        """
        Selects the radio button if it's not already selected

        Returns:
            None

        """
        if not self.is_selected():
            self.click()

