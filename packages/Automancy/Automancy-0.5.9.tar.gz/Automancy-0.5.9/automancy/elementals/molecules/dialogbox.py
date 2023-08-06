""" ./elementals/molecules/dialogbox.py """
from automancy.core import Elemental, Model


class DialogBox(Elemental, Model):
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)
        self.confirm_button = None
        self.negate_button = None
        self.message = ''
        self.title = ''
        self.special_option = ''

    def confirm(self) -> None:
        """ Clicks the Yes/Confirm/Etc button when assigned """
        if self.confirm_button:
            self.confirm_button.click()

    def negate(self) -> None:
        """ Clicks the No/Cancel/Etc button when assigned """
        if self.negate_button:
            self.negate_button.click()
