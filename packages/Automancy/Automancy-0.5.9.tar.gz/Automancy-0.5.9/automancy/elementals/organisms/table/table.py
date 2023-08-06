from automancy.core import Elemental

from .table_body import TableBody
from .table_header import TableHeader
from .table_options import TableOptions


class Table(Elemental):
    """ Organism Table for collections of smaller Elementals that make up a Table (rows usually) """
    def __init__(self, locator, human_name, system_name, options=TableOptions()):
        """

        Notes:
            Conventional thinking would suggest that options could/should simply be a dictionary.  While this
            sounds more simple than using an explicitly defined "option" class, you lose operational performance
            and the ability to maintain contractual rules for options with a dictionary.  Don't be lazy sucka!

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            options (TableOptions): An options object that contains some of it's own logic and is ideally hot-swappable.

        """
        super().__init__(locator, human_name, system_name)

        # Make sure that the options object is an instance of TableOptions before proceeding
        if not isinstance(options, TableOptions):
            raise TypeError('The value of "options" must be of type "TableOptions".  Thought you were sneaky did ya?...')

        # Save the options object
        self.options = options

        # Define the components dictionary
        self.row_components = []

        # Header contains a reference to all column names as a list as seen to the user.
        self.header = TableHeader(self.locator + self.options.header_locator, self.name, self.system_name, cell_locator=self.options.header_cell_locator)
        self.body = TableBody(self.options.body_locator, self.name, self.system_name, rows_locator=self.options.body_row_locator, cell_locator=self.options.body_row_cell_locator)

    def __iter__(self):
        """ Return an iterator for Table.body.rows but explicitly tell the user that they must perform .read() first... explicitly ... """
        if not self.rows:
            raise ValueError('No table rows detected.  Ensure that you perform .read() on this instance ("{table_name}") first before iterating over it'.format(table_name=self.name))

        return iter(self.rows)

    def __len__(self):
        return len(self.body) if self.body else 0

    @property
    def rows(self):
        """
        Used when all you care about is a shortcut to access the rows in the table

        Returns:
            list: The list of rows held in Table.body.rows

        """
        return self.body.rows

    @property
    def row_count(self):
        """
        Get the number of rows within the table body right now.

        Returns:
            (int): The number of rows in the table body.

        """
        self.read()
        return len(self)

    def include(self, component):
        """
        Adds a Elemental to the Table's row_components dictionary and the name of the component to the header columns list.

        The Table instance must have the 'manual_components' option set to True in order for include() to be used.

        Notes:
            The row_components property is a container that holds objects that can be added as instance properties of each row.

        Args:
            component (Elemental, Dropdown): The Automancy object that is being added as a component

        """
        # Make sure that options.manual_components is True for this instance before allowing components to be added
        if not self.options.manual_components:
            raise AttributeError('This Table object does not allow the manual definition of row components.  Change "...options.manual_components" for this instance to True and retry.')

        # Make sure that the Automancy object we're attempting to include is properly named before allowing components to be added
        if component.name == '':
            raise ValueError('Automancy objects must be properly named in order to use the name as the header key, empty string\'s not allowed.')

        # Make sure that the component name is within the header.
        if component.name not in self.header.columns:
            # Add the object name to the header columns
            self.header.columns.append(component.name)
            # Add the object to the row components
            self.row_components.append(component)

    def add_components(self):
        """ Adds components known in Table.row_components to all known rows """
        # Loops through each of the manual component to each of the rows using a deep copy method
        for component in self.row_components:
            for index, row in enumerate(self.body.rows, start=1):

                # Construct the entire xpath locator for each row component based on row index
                full_component_locator = '{table_root}{body}{row}[{index}]{component}'.format(
                    table_root=self.locator,
                    body=self.body.locator,
                    row=row.locator,
                    index=index,
                    component=component.locator
                )

                # Duplicate the component object and update it's locator
                row.cells[component.name] = component.duplicate()
                row[component.name].locator = full_component_locator

    def values(self):
        """
        Same functionality as dict().values() but returns the body's rows, or None

        Returns:
            list,None:

        """
        if self.body:
            return self.body.rows
        else:
            return None

    def column(self, column_name):
        """
        Looks at a single column named by the argument to get a list of the strings in each of the cells

        Notes:
            The table must have been read first with the Table.read() method.
            If if the column name doesn't exist, returns an empty list.
            If a cell in the table doesn't contain any text, an empty string will be returned to represent that cell.

        Args:
            column_name (str): The name of the column that you want the contents of.

        Returns:
            list: of strings representing the text content of the cells in the named column.

        """
        column_values = []
        if self.body:

            if len(self.body) <= 0:
                print('No table body rows detected, please run Table.body.get_rows() first')
                return column_values

            if column_name not in self.header.columns:
                print('The search term ({0}) does not match any column labels ({1})'.format(column_name, self.header.columns))
                return column_values

            column_values = [row[column_name].text for row in self.body.rows]

        return column_values

    def read(self, get_text_now=False):
        """
        Updates the Table instance through construction of the rows and row cell Elementals
        as well as some of the contextual data such as header column text and cell text (if any)

        Simply put: One method call, that's all.

        Notes:
            Table.body.rows is reset to an empty list.  This is done in order
            to get a fresh read on the table.  Without this, the rows object
            would simply be appended to, effectively doubling the real amount
            of rows.

            Table.header.columns will be a list of strings that represent
            the column name/identifier.

            Table.body.rows will be a list of TableRow instances.
            Each TableRow instance will will have a property called "cells"

            TableRow.cells is a dictionary of header column name keys and
            Cell Elemental instance values.

            The "text" property of each Cell instance will contain the text
            as it is displayed in the DOM.

            Each nested object(s) have a reference to the header columns
            which are used to refer to the overall structure.

        """
        # Clear any stored rows
        self.body.rows = []

        # If the manual_component flag is True, we are going to read each row using row_components
        if self.options.manual_components:
            self.body.get_rows()
            self.add_components()
        else:
            # Define what the table header columns are.
            self.header.define_columns()

            # Construct the objects that make up the rows and row cells for the table body
            self.body.header = self.header.columns
            self.body.get_rows()
            # self.body.get_cells(get_text_now=get_text_now)

            # Constructs each of the cells for each row that is known in the table
            if self.body.rows:
                for row in self.body.rows:
                    row.get_cells(self.body.header, get_text_now=get_text_now)

    def find_cell(self, search_term):
        """
        Searches the entire table for the search term string.

        Args:
            search_term (str): The string to look for in the cells text

        Returns:
            tuple: Tuple of the row and column identifier or empty if not found

        """

        if len(self.body) <= 0:
            print('WARNING: No table body rows detected, please run Table.body.get_rows() first')
            return tuple()

        for row_num, row in enumerate(self.body.rows):
            if len(row) <= 0:
                print('WARNING: No row cells detected for row {0}.  Please run Row.get_cells() on this row first.'.format(row.name))
                break

            for cell_num, cell in enumerate(row.cells):
                if search_term in cell.text:
                    return row_num, cell_num

        return tuple()

    def find_in_column(self, column_name, search_term):
        """
        Searches within a specified column for the search term and a list of rows where the search term matches.

        Args:
            column_name (str): Target column
            search_term (str): String that you're looking for the row that it exists in

        Returns: The rows that contains the search string as a list, or as a single Row object if there is only one.

        """
        column_values = self.column(column_name)

        if len(column_values) < len(self.body):
            print('ERROR: The length of found column values ({0}) is less than the number of rows ({1}), investigate discrepancy.'.format(
                len(column_values),
                len(self.body)
            ))

        matching_rows = []

        for value_num, value in enumerate(column_values):
            if search_term == value:
                matching_rows.append(self.body.rows[value_num])

        if len(matching_rows) == 1:
            matching_rows = matching_rows[0]

        return matching_rows
