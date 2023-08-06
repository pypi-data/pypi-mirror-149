""" ./elementals/organisms/calendar/calendar_month.py """
from automancy.core import Elemental
from .calendar_options import CalendarOptions


class CalendarMonth(Elemental):
    """ CalendarMonth objects are used to store week and day arrays for each month that is visually displayed within the containing Calendar object"""
    def __init__(self, locator: str, human_name: str, system_name: str, options: CalendarOptions = CalendarOptions()):
        super().__init__(locator, human_name, system_name)
        self.options = options
        self.day_cell_locator = None
        self.week_row_locator = None

        self.set_options(self.options)

    def set_options(self, options):
        """
        Allows an already instantiated Calendar object to have it's options reconfigured as needed

        Args:
            options (CalendarOptions): The base options object that is used to to construct the required components of a Calendar object

        Returns:
            None

        """
        # Prevent instantiation if the options object isn't of a CalendarOptions type
        if not isinstance(options, CalendarOptions):
            raise TypeError('Must provide a CalendarOptions object as the second argument when constructing a Calendar object.  Object type received: {0}'.format(type(options)))

        # Store the instance of CalenderOptions within this Calendar instance
        self.options = options

        # Store whatever locator values by themselves that exist which might be used later (depends on use cases)
        self.day_cell_locator = options.day_cell_locator
        self.week_row_locator = options.week_row_locator
