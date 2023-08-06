""" ./elementals/organisms/calendar/calendar_options.py """


class CalendarOptions(object):
    """
    An options object to be used when creating a new Calendar object to interact with.

    XPath strings to specific elements of a calendar are stored in one of these objects
    and then looked for during the construction of a Calendar object itself.
    """
    def __init__(self, **kwargs):
        self.current_month_locator = kwargs['current_month_locator'] if 'current_month_locator' in kwargs.keys() else ''
        self.day_cell_locator = kwargs['day_cell_locator'] if 'day_cell_locator' in kwargs.keys() else ''
        self.week_row_locator = kwargs['week_row_locator'] if 'week_row_locator' in kwargs.keys() else ''
        self.month_next_locator = kwargs['month_next_locator'] if 'month_next_locator' in kwargs.keys() else ''
        self.month_prev_locator = kwargs['month_prev_locator'] if 'month_prev_locator' in kwargs.keys() else ''
        self.save_button_locator = kwargs['save_button_locator'] if 'save_button_locator' in kwargs.keys() else ''
        self.cancel_button_locator = kwargs['cancel_button_locator'] if 'cancel_button_locator' in kwargs.keys() else ''
        self.month_style = kwargs['month_style'] if 'month_style' in kwargs.keys() else 'single'
