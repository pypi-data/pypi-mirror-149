from .table_row import TableRow


class TableHeader(TableRow):
    """ Object that represents the header of a table """
    def __init__(self, locator, human_name, system_name, cell_locator='//td'):
        super().__init__(locator, human_name, system_name)

        # The locator for columns in the header.
        self.cell_locator = cell_locator

        # Content contains strings of the names of the columns as they appear to the user
        self.columns = []

    def define_columns(self):
        """
        If TableHeader.columns is empty, create a list of the text for each column of the row.

        Returns:
            list: Strings representing the names for each column.

        """

        if len(self.columns) > 0:
            print('WARNING: Header for this table is already populated, preventing over-write attempt.')
            return self.columns

        for cell_num, cell in enumerate(self):
            cell_text = cell.text

            if cell_text == '':
                cell_text = 'Unnamed{num}'.format(num=cell_num)

            self.columns.append(cell_text)

        return self.columns
