""" ./elementals/organisms/calendar/option_tree_branch.py """
from automancy.core import Elemental


class OptionTreeBranch(Elemental):
    """ Container for a single option within an option tree """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name

        """
        super().__init__(locator, human_name, system_name)
        self.collapsible = False
        self.collapser = None
        self.label = ''
        self.selector = locator
