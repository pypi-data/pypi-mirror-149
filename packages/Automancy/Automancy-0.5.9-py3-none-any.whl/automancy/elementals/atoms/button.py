""" ./atoms/button.py """
from automancy.core import Elemental


class Button(Elemental):
    """ Atom Elemental for button DOM objects """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Represents a basic button DOM element of any kind which could exist on a page.

        It's not a sin to use this class for anything which you might think as a button
        but isn't necessarily a <button> element.

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)
