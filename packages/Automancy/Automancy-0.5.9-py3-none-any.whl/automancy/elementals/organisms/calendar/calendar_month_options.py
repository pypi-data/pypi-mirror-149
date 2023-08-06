""" ./elementals/organisms/calendar/calendar_month_options.py """


class CalendarMonthOptions(object):
    """
    An options object to be used when creating a new CalendarMonth object to interact with.

    XPath strings to specific elements of a calendar are stored in one of these objects
    and then looked for during the construction of a CalendarMonth object itself.
    """
    def __init__(self, **kwargs):
        self.day_cell_locator = kwargs['day_cell_locator'] if 'day_cell_locator' in kwargs.keys() else ''
        self.week_row_locator = kwargs['week_row_locator'] if 'week_row_locator' in kwargs.keys() else ''

