

class TableOptions(object):
    """
    Options context object for optional parameters used by a Table object within Automancy.

    It is strongly recommended that the number of arguments for a class not exceed 7 as a
    best practice.

    From SonarLint:
    "A long parameter list can indicate that a new structure should be created to wrap the
    numerous parameters or that the function is doing too many things."

    Additionally, this object allows pre-defined option sets that can be swapped in/out of
    it's paired class, or used in a one-to-many, many-to-one, or many-to-many fashion between
    different instances of TableOptions and Table.
    """
    def __init__(self, **kwargs):
        """
        Default values are defined through logic if their kwarg counterpart does not exist or
        is not defined.

        Keyword Args:
            manual_components (bool):
            header_locator (str):
            header_cell_locator (str):
            body_locator (str):
            body_row_locator (str):
            body_row_cell_locator (str):

        """
        self.manual_components = kwargs['manual_components'] if 'manual_components' in kwargs else False
        self.header_locator = kwargs['header_locator'] if 'header_locator' in kwargs else '//thead/tr'
        self.header_cell_locator = kwargs['header_cell_locator'] if 'header_cell_locator' in kwargs else '//th'
        self.body_locator = kwargs['body_locator'] if 'body_locator' in kwargs else '//tbody'
        self.body_row_locator = kwargs['body_row_locator'] if 'body_row_locator' in kwargs else '//tr'
        self.body_row_cell_locator = kwargs['body_row_cell_locator'] if 'body_row_cell_locator' in kwargs else '//td'
