""" ./atoms/switch.py """
from automancy.core import Elemental


class Switch(Elemental):
    """ Atom Elemental for switch form option DOM objects """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Represents a switch form options DOM element which can only be on or off.

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)

    def flip(self):
        """ If the position is off, flip it on.  If on, flip it off.  Duh... """
        self.click()
