from automancy.core import Elemental


class TableCell(Elemental):
    """ Molecule Elemental for Row web elements """
    def __init__(self, locator, human_name, system_name, cell_type=None):
        """
        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            cell_type (): Optional, an Automancy based object (i.e., Button, Dropdown, etc) that the cell is

        """
        super().__init__(locator, human_name, system_name)
        self.color = ''
        self.icon = None

        # E.g. Button, Label, Checkbox, etc (Any Automancy atom type)
        self.type = cell_type
