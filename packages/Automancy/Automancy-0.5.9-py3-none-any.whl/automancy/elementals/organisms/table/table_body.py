from typing import List

from automancy.core import Elemental
from .table_row import TableRow


class TableBody(Elemental):
    """ Object that represents the body of a table.  Includes a reference to the names of the columns """
    def __init__(self, locator, human_name, system_name, parent_locator='/ancestor::table[1]', rows_locator='//tr', cell_locator='//td'):
        super().__init__(locator, human_name, system_name)

        self.header = []
        self.rows = []
        self.parent_locator = parent_locator
        self.rows_locator = rows_locator
        self.cell_locator = cell_locator

        # The string related to the header column text for the cell that is used to mark the row "selected"
        self.row_selector = ''
        self.row_selector_special_modifier = ''

    def __len__(self):
        if self.rows:
            return len(self.rows)
        else:
            return 0

    def deselect_all(self):
        """
        Deselects all rows that are currently selected.
        """
        for row in self.rows:
            if row.selected:
                row.deselect()

    @staticmethod
    def select_rows(rows: List[TableRow]):
        """
        Selects any number of assets in the containing rows list by it's checkbox

        Args:
            rows (List[Row]): List of Row Elementals that will selected

        """
        for row in rows:
            row.select()

    @staticmethod
    def deselect_rows(rows: List[TableRow]):
        """
        Inverse of TableBody.select_rows()

        Args:
            rows (List[Row]):

        """
        for row in rows:
            row.deselect()

    def get_rows(self):
        """
        Finds all of the rows in the table body and appends them to self.rows
        """
        rows = self.find_elements(self.locator + self.rows_locator)

        # The Firefox (Gecko) WebDriver is the worst and for some reason detect a trailing element that doesn't exist.
        # TODO -> This is a shitty way to do this.  Redesign this to be more generic, perhaps making sure that the element has expected content.
        if 'firefox' in self.browser_used and len(rows) > 1:
            del rows[-1]

        if rows:
            for row_num, row in enumerate(rows, start=1):
                name = 'row{row_num}'.format(row_num=row_num)
                locator = self.rows_locator + '[{row_num}]'.format(row_num=row_num)

                # Define the new row and append to list
                new_row = TableRow(locator, name, name, cell_locator=self.cell_locator, header=self.header, selector=self.row_selector)

                if self.row_selector_special_modifier:
                    new_row.selector_special_modifier = self.row_selector_special_modifier

                self.rows.append(new_row)
        else:
            print('WARNING: No rows were found using the xpath locator: {0}'.format(self.locator + self.rows_locator))
