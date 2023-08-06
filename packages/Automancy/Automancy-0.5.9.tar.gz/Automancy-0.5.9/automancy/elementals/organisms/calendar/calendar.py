""" ./elementals/organisms/calendar/calendar.py """
from selenium.webdriver.common.by import By

from automancy.core import Elemental
from automancy.elementals.atoms import Button, Label
from automancy.core.tactical_asserts import TacticalAsserts

from .calendar_day import CalendarDay
from .calendar_week import CalendarWeek
from .calendar_options import CalendarOptions


class Calendar(Elemental):
    """ The prime object which houses and links all other calendar based object """

    def __init__(self, locator, human_name, system_name, options=CalendarOptions()):
        super().__init__(locator, human_name, system_name)
        self.asserts = TacticalAsserts()
        self.options = options
        self.month_style = None

        # XPath locator strings that we're retaining knowledge of for object independent use
        self.day_cell_locator = None
        self.week_row_locator = None

        # Containers for interactable objects if they are defined with this.set_options()
        self.current_month = None
        self.save_button = None
        self.cancel_button = None
        self.month_prev_button = None
        self.month_next_button = None

        # Arrays that contain the interactable week and day objects
        self.weeks = []
        self.days = []

        # Do the initial setup for this objects values.
        self.set_options(self.options)

    def construct_weeks(self):
        """
        Construct the array of web elements that constitutes the weeks of the currently viewed month

        Returns:
            None

        """
        # Make sure that we have a locator for the week elements
        if not self.week_row_locator:
            raise ValueError('An Xpath locator string must be supplied that allows each of the calendar weeks to be found in the DOM, None found')

        # Clear the internal weeks array to reset the state
        self.weeks = []

        # Find the elements in the DOM that represent each of the weeks
        found_week_elements = self.browser.find_elements(By.XPATH, self.locator + self.week_row_locator)

        # Construct objects and their individual locators based on the index that they're found at.
        for index, week in enumerate(found_week_elements, start=1):
            this_week = CalendarWeek(self.locator + self.week_row_locator + '[{}]'.format(index), 'Week {}'.format(index), 'week_{}'.format(index))

            # It's possible for a Selenium to pick up more weeks than actually exist in the DOM, ensure that we only get real existing weeks.
            if this_week.exists:
                self.weeks.append(this_week)

    def pre_process_days(self):
        # Make sure that we have a locator for the day elements
        if not self.day_cell_locator:
            raise ValueError('An Xpath locator string must be supplied that allows each of the calendar days to be found in the DOM, None found')

        # This container holds all days found for this calendar object before the preceding and trailing days from the preceding and trailing months
        pre_processed_days = []

        # Construct the week objects if they have not been already
        if not self.weeks:
            self.construct_weeks()

        # Iterate through each week to construct the objects for each day along with each individual locator
        for week in self.weeks:
            found_days = week.find_elements(week.locator + self.day_cell_locator)

            for day_num, day in enumerate(found_days, start=1):
                this_day = CalendarDay(week.locator + self.day_cell_locator + '[{}]'.format(day_num), 'Day {}'.format(day_num), 'day_{}'.format(day_num))

                # It's possible for a Selenium to pick up more days than actually exist in the DOM, ensure that we only get real existing weeks.
                if this_day.exists:
                    pre_processed_days.append(this_day)

        return pre_processed_days

    @staticmethod
    def is_first_day_of_month(day_text):
        return True if day_text == '1' or day_text == '01' else False

    def construct_days(self):
        """
        Takes the values for the week and day locators and constructs arrays of interactable objects based on which month is visible to the user

        Returns:
            None

        """
        # Becomes True when the first day of the month is discovered (sometimes first month discovered is last day(s) of previous month)
        first_day_found = False

        # Iterate over each day to remove the dates from the previous month and the following month
        for day_num, day in enumerate(self.pre_process_days()):
            # Store the text value of the day element
            day_text = day.text.strip(' ')

            if Calendar.is_first_day_of_month(day_text):
                # Stop processing the days of the month when we encounter the first day of the following month (calender bleed over)
                if first_day_found:
                    break

                # Check to see if this is the first real day of the month and set the flag
                first_day_found = True

            # Make sure that we're only working on days within the month and not in the month before
            if first_day_found:
                # Update the internal name of the day object
                day.name = 'Day{}'.format(day_num)

                # Append the day object to the self.days array
                self.days.append(day)

    def next_month(self, get_days_now=False):
        """
        Clicks on the button that changes the month forward by one

        Args:
            get_days_now (bool): If true, the week and day objects will be constructed for the new month immediately.

        Returns:
            None

        """
        if self.month_next_button:
            self.asserts.becomes_interactable(self.month_next_button).click()

            # Reset the days and weeks known by the Calendar object instance when changing months
            self.days = []
            self.weeks = []

            # If this optional flag is set, automatically construct the day objects for the month
            if get_days_now:
                self.construct_days()

    def prev_month(self, get_days_now=False):
        """
        Clicks on the button that changes the month back by one

        Args:
            get_days_now (bool): If true, the week and day objects will be constructed for the new month immediately.

        Returns:
            None

        """
        if self.month_prev_button:
            self.asserts.becomes_interactable(self.month_prev_button).click()

            # Reset the days and weeks known by the Calendar object instance when changing months
            self.days = []
            self.weeks = []

            # If this optional flag is set, automatically construct the day objects for the month
            if get_days_now:
                self.construct_days()

    def select_day(self, day, save=False):
        """
        Clicks the element that represents the day of the month which the user wishes to select.

        The day argument must be an integer.

        Args:
            day (int): The day of the month that you wish to click on to select
            save (bool): Optional, if True, the calendar save button is clicked after date selection

        Returns:
            None

        """
        # Ensure that the parameter is an integer (and nothing else jerk!)
        if not isinstance(day, int):
            raise TypeError('The "day" argument must be an integer value')

        # Construct the day objects if they haven't been already
        if not self.days:
            self.construct_days()

        # Ensure that the date input value is between the number of days in the current month
        if not 0 < day <= len(self.days):
            raise ValueError('The "day" parameter must be between 1 and {} days'.format(len(self.days)))

        # Ensure that the element for the desired day is interactable before clicking on it
        self.asserts.becomes_interactable(self.days[day - 1]).click()

        if save:
            self.save()

    def select_range(self, start_month, start_day, end_month, end_day):
        """
        Handles the selection of a start and end date in order to select a range of dates

        Args:
            start_month (CalendarMonth):
            start_day (int):
            end_month (CalendarMonth):
            end_day (int):

        Returns:
            None

        """
        raise NotImplementedError

    def save(self):
        """ Clicks the Button object for save_button if the attribute is defined """
        if not self.save_button:
            raise AttributeError('Save button component is not defined, cannot click the "save" button to save calender changes')

        self.asserts.becomes_interactable(self.save_button).click()

    def cancel(self):
        """ Clicks the Button object for cancel_button if the attribute is defined """
        if not self.cancel_button:
            raise AttributeError('Cancel button component is not defined, cannot click the "cancel" button to cancel calender changes')

        self.asserts.becomes_interactable(self.cancel_button).click()

    def set_options(self, options: CalendarOptions):
        """
        Allows an already instantiated Calendar object to have it's options reconfigured as needed

        Args:
            options (CalendarOptions): The base options object that is used to to construct the required components of a Calendar object

        Returns:
            None

        """
        if not isinstance(options, CalendarOptions):
            raise TypeError('Must provide a CalendarOptions object as the second argument when constructing a Calendar object.  Object type received: {0}'.format(type(options)))

        # Store whatever locator values by themselves that exist which might be used later (depends on use cases)
        self.day_cell_locator = options.day_cell_locator
        self.week_row_locator = options.week_row_locator

        # Define the month style which is to be either 'single' or 'double'
        self.month_style = options.month_style

        # Define the Label object for the current month label element if the locator is defined
        if options.current_month_locator:
            self.current_month = Label(self.locator + options.current_month_locator, 'Current Month', 'current_month')

        # Define the Button object for the previous month button element if the locator is defined
        if options.month_prev_locator:
            self.month_prev_button = Button(self.locator + options.month_prev_locator, 'Previous Month Button', 'month_prev_button')

        # Define the Button object for the next month button element if the locator is defined
        if options.month_next_locator:
            self.month_next_button = Button(self.locator + options.month_next_locator, 'Next Month Button', 'month_next_button')

        if options.save_button_locator:
            self.save_button = Button(self.locator + options.save_button_locator, 'Save Button', 'save_button')

        if options.cancel_button_locator:
            self.cancel_button = Button(self.locator + options.cancel_button_locator, 'Cancel Button', 'cancel_button')

    @staticmethod
    def day_with_suffix(day):
        """ Return the date as a string with the correct 'st', 'nd', 'rd', or 'th' suffix after the number """

        # Ensure that the input value can only be an integer or string type
        if not isinstance(day, int):
            raise TypeError('The value for "Day" must be an integer or a string that is only an integer, found type: {}'.format(type(day)))

        # Ensure that that if the input is a string, that the string is a only digit
        if isinstance(day, str) and not day.isdigit():
            raise ValueError('Input value was detected as a non digit string.  Input must pass day.isdigit().  Found value: {}'.format(day))

        # Convert the day number to an integer if it was sent in as a string
        if isinstance(day, str):
            day = int(day)

        st = '{}st'
        nd = '{}nd'
        rd = '{}rd'
        th = '{}th'
        return th.format(day) if 11 <= day <= 13 else {1: st.format(day), 2: nd.format(day), 3: rd.format(day)}.get(day % 10, th.format(day))
