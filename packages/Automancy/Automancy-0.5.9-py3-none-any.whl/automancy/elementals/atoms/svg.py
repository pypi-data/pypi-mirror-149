""" ./atoms/svg.py """
from automancy.core import Elemental
from automancy.core.tactical_asserts import TacticalAsserts


class SVG(Elemental):
    """ Atom Elemental for <svg>> DOM objects """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Constructicons!  Merge for the kill!!!

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)
        self.paths = []
        self.__asserts = TacticalAsserts()

    def find_paths(self):
        """ Internally searches the element for <path> elements and adds them to the self.path list """
        self.__asserts.gains_visibility(self)
        return self.find_elements('//path')


class SVGPath(Elemental):
    """ Object that represents a <path> sub-element of an <svg> element """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Wait! The Constructicons form Devastator, the most powerful robot. We should rule!

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)
        self._d = ''

    @property
    def d(self):
        return self.properties()['d']
