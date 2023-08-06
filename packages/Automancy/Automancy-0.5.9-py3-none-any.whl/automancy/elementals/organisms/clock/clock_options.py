""" ./elementals/organisms/calendar/clock_options.py """


class ClockOptions(object):
    """
    An options object to be used when creating a new Calendar object to interact with.

    XPath strings to specific elements of a calendar are stored in one of these objects
    and then looked for during the construction of a Calendar object itself.
    """
    def __init__(self, **kwargs):
        self.current_hour_locator = kwargs['current_hour_locator'] if 'current_hour_locator' in kwargs.keys() else ''
        self.current_minute_locator = kwargs['current_minute_locator'] if 'current_minute_locator' in kwargs.keys() else ''
        self.clock_face_locator = kwargs['clock_face_locator'] if 'clock_face_locator' in kwargs.keys() else ''
        self.save_button_locator = kwargs['save_button_locator'] if 'save_button_locator' in kwargs.keys() else ''
        self.cancel_button_locator = kwargs['cancel_button_locator'] if 'cancel_button_locator' in kwargs.keys() else ''
        self.hour_zero_locator = kwargs['hour_zero_locator'] if 'hour_zero_locator' in kwargs.keys() else ''
        self.minute_zero_locator = kwargs['minute_zero_locator'] if 'minute_zero_locator' in kwargs.keys() else ''
        self.am_locator = kwargs['am_locator'] if 'am_locator' in kwargs.keys() else ''
        self.pm_locator = kwargs['pm_locator'] if 'pm_locator' in kwargs.keys() else ''
        self.hour_format = kwargs['hour_format'] if 'hour_format' in kwargs.keys() else 12
