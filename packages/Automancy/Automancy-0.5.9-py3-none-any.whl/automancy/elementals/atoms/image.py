""" ./atoms/image.py"""
from automancy.core import Elemental


class Image(Elemental):
    """ Atom Elemental for <img> DOM objects """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)

    @property
    def src(self):
        """ Returns the src attribute value of this <img> element """
        return self.element().get_attribute('src')
