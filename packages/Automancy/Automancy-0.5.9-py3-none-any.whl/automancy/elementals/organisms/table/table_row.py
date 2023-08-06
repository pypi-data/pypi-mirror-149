from lxml.etree import XPath, XPathSyntaxError

from automancy.core import Elemental
from .table_cell import TableCell


class TableRow(Elemental):
    """ Molecule Elemental for Row web elements """
    def __init__(self, locator, human_name, system_name, cell_locator='', header=None, selector=''):
        """
        Notes:
            Rows are things like Table rows, Dropdown option rows, etc

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            cell_locator ():
            header ():
            selector ():

        """
        super().__init__(locator, human_name, system_name)

        self.cell_locator = cell_locator
        self.cells = {}
        self.header = header
        self.selector_column = selector
        self.selector_object = None
        self.selector_special_modifier = ''

        self.selected = False

        # As a special consideration, this can be populated with references to the Elemental
        # types that are expected to exist in each cell for a row.
        # Example: [Button, Label, Label, Image, Link]
        # This example implies that there are five cells in a row and that the first cell is a button
        # the second and third cells are Labels, the fourth is an Image, and the fifth is a Link.
        self.expected_objects = []

    def __getitem__(self, item):
        return self.cells[item]

    def __setitem__(self, key, value):
        self.cells[key] = value

    def __len__(self):
        return len(self.cells)

    def values(self):
        """
        Same functionality as dict().values() but returns the rows' cells, or None

        Returns:
            list, None:

        """
        if self.cells:
            return self.cells.values()
        else:
            return None

    def select(self):
        """
        When used, the object considered the "selector for the row will be clicked
        and the row should then be considered selected on the page.
        """
        if not self.selected:
            if self.selector_object:
                self.selector_object.click()
                self.selected = True
            else:
                print('ERROR: Selector object for this table row is not defined, cannot select it.')
        else:
            print('WARNING: Attempting to select a row that is believed to be already selected')

    def deselect(self):
        """
        Inverse of Row.select()
        """
        if self.selected:
            if self.selector_object:
                self.selector_object.click()
                self.selected = False
            print('ERROR: Selector object for this table row is not defined, cannot select it.')
        else:
            print('WARNING: Attempting to deselect a row that is believed to be currently not selected')

    @staticmethod
    def modify_locator(original, extension):
        """
        Some situations call for a modified xpath string for row selector objects.

        This method is used to combine the original locator with an extension,
        making sure that the combined string is valid XPath syntax

        Args:
            original (str): The original locator XPath string for the Elemental
            extension (str): The XPath extension string to be concatenated.

        Returns:
            str: Combined XPath string after validation

        """
        try:
            modified_locator = XPath(original + extension).path
            return modified_locator
        except XPathSyntaxError:
            raise ValueError('Bad XPath syntax detected while attempting to add a special modifier for a table row selector. --- Attempted: {0}{1}'.format(original, extension))

    def get_cells(self, header):
        """
        Goes through all of the cells in the row and populates the object self.cells with Cell type Elementals.

        Does not interact with the Selenium WebElements here for the cell elements, only to get a count of the
        number of cell elements that are found in the row element

        Args:
            header (list): List of strings considered to be the keys for each cell

        """
        if self.cell_locator:

            # Find all of the WebElements that we expect to use on the DOM
            cells = self.find_elements(self.locator + self.cell_locator)

            # The Firefox (Gecko) WebDriver is the worst and for some reason detect a trailing element that doesn't exist.
            # TODO -> This is a shitty way to do this.  Redesign this to be more generic, perhaps making sure that the element has expected content.
            if 'firefox' in self.browser_used and len(cells) > 1:
                del cells[-1]

            # Strip all returned elements above the expected number of header elements
            del cells[len(header):]

            for cell_num, cell in enumerate(cells):
                name = 'cell{cell_num}'.format(cell_num=cell_num+1)
                locator = self.locator + self.cell_locator + '[{cell_num}]'.format(cell_num=cell_num+1)

                # Construct the Cell object while getting the elements interior text.
                new_cell = TableCell(locator, name, name)

                # Add the new cell to this rows list of known cells
                self[header[cell_num]] = new_cell

                # If this cell is in the column matching the selector column text, make this cell the selector object.
                if header[cell_num] == self.selector_column:

                    # If a special modifier has been defined, modify the row locator xpath
                    if self.selector_special_modifier:
                        new_cell.locator = self.modify_locator(locator, self.selector_special_modifier)

                    self.selector_object = new_cell
