""" ./elementals/organisms/calendar/clock.py """
import math

from selenium.webdriver.common.action_chains import ActionChains

from automancy.core import Elemental
from automancy.core.tactical_asserts import TacticalAsserts
from automancy.elementals import Button, Label
from automancy.elementals.organisms.clock.clock_options import ClockOptions


class Clock(Elemental):
    """ The prime object which houses and links all other calendar based object """
    def __init__(self, locator, human_name: str, system_name: str, options: ClockOptions = ClockOptions()):
        super().__init__(locator, human_name, system_name)
        self.__asserts = TacticalAsserts()
        self.options = options
        self.time_style = None

        # Containers for interactable objects if they are defined with this.set_options()
        self.current_hour = None
        self.current_minute = None
        self.clock_face = None
        self.save_button = None
        self.cancel_button = None
        self.hour_zero_element = None
        self.minute_zero_element = None
        self.am_element = None
        self.pm_element = None

        # Built in property
        self._hour_format = 13

        # Do the initial setup for this objects values.
        self.set_options(options)

    @property
    def hour_format(self):
        return self._hour_format

    @hour_format.setter
    def hour_format(self, value):
        # Make sure that value is an integer in cases where people think it's cool to use numbers in strings...
        try:
            value = int(value)

            # Make sure that the value is either 12 or 24 to indicate the only two acceptable hour formats
            if value != 12 and value != 24:
                raise ValueError('Clock.hour_format must be either 12 or 24. Value received: {}'.format(value))

            self._hour_format = value

        # Catch those jerks when they attempt to use anything but an int or a string
        except TypeError:
            raise TypeError('Clock.hour_format must be an integer or a string.  Object type received: {}'.format(type(value)))

    def save(self):
        """ Clicks the Button object for save_button if the attribute is defined """
        if not self.save_button:
            raise AttributeError('Save button component is not defined, cannot click the "save" button to save calender changes')

        self.__asserts.becomes_interactable(self.save_button).click()

    def cancel(self):
        """ Clicks the Button object for cancel_button if the attribute is defined """
        if not self.cancel_button:
            raise AttributeError('Cancel button component is not defined, cannot click the "cancel" button to cancel calender changes')

        self.__asserts.becomes_interactable(self.cancel_button).click()

    def set_options(self, options):
        """
        Allows an already instantiated Calendar object to have it's options reconfigured as needed

        Args:
            options (CalendarOptions): The base options object that is used to to construct the required components of a Calendar object

        Returns:
            None

        """
        # Prevent instantiation if the options object isn't of a CalendarOptions type
        if not isinstance(options, ClockOptions):
            raise TypeError('Must provide a CalendarOptions object as the second argument when constructing a Calendar object.  Object type received: {0}'.format(type(options)))

        # Store the instance of CalenderOptions within this Calendar instance
        self.options = options
        self.current_hour = Label(self.locator + options.current_hour_locator, 'Clock Current Hour', 'current_hour') if options.current_hour_locator else None
        self.current_minute = Label(self.locator + options.current_minute_locator, 'Clock Current Minute', 'current_minute') if options.current_minute_locator else None
        self.clock_face = Elemental(self.locator + options.clock_face_locator, 'Clock Face', 'clock_face') if options.clock_face_locator else None
        self.save_button = Button(self.locator + options.save_button_locator, 'Clock Save Button', 'save_button') if options.save_button_locator else None
        self.cancel_button = Button(self.locator + options.cancel_button_locator, 'Clock Cancel Button', 'cancel_button') if options.cancel_button_locator else None
        self.hour_zero_element = Button(self.locator + options.hour_zero_locator, 'Clock Hour Zero Element', 'hour_zero_element') if options.hour_zero_locator else None
        self.minute_zero_element = Button(self.locator + options.minute_zero_locator, 'Clock Minute Zero Element', 'minute_zero_element') if options.minute_zero_locator else None
        self.am_element = Button(self.locator + options.am_locator, 'AM Element', 'am_element') if options.am_locator else None
        self.pm_element = Button(self.locator + options.pm_locator, 'PM Element', 'pm_element') if options.pm_locator else None

        # In the case that the minute zero element isn't defined, we can assume that it's the same location as the hour zero element use it for positional reference
        if not self.minute_zero_element:
            self.minute_zero_element = self.hour_zero_element

        # Ensure that the hour format value is either 12 or 24 as an integer.  If not, default to 12
        if int(options.hour_format) == 12 or int(options.hour_format) == 24:
            self.hour_format = int(options.hour_format)
        else:
            self.hour_format = 12

    def click_on_hour(self, hour):
        """
        Performs a selenium action chain click event to select an hour on the clock face by
        clicking at a position that is an offset from the top-left 0,0 coordinate of the
        clock face element

        Args:
            hour (int): The hour to be selected on the clock face

        Returns:
            None

        """
        angle = self.hour_to_angle(int(hour))
        coords = self.end_coords_of_angle(angle)
        action = ActionChains(self.browser)
        action.move_to_element_with_offset(self.clock_face.element(), coords['x'], coords['y'])
        action.click()
        action.perform()

    def click_on_minute(self, minute):
        """
        Performs a selenium action chain click event to select an minute on the clock face by
        clicking at a position that is an offset from the top-left 0,0 coordinate of the
        clock face element

        Args:
            minute (int): The minute to be selected on the clock face

        Returns:
            None

        """
        angle = self.minute_to_angle(minute)
        coords = self.end_coords_of_angle(angle)
        action = ActionChains(self.browser)
        action.move_to_element_with_offset(self.clock_face.element(), coords['x'], coords['y'])
        action.click()
        action.perform()

    def hour_to_angle(self, choice):
        """
        Converts an hour number (12 or 24) into the angle degree in a circle

        Args:
            choice (int): Between 1 to 12 or 1 to 24 depending on the clock face type (12-hour / 24-hour)

        Returns:
            float: The angle degree of the hour selection

        """
        degree = (360 / self.hour_format) * int(choice)
        return 0 if degree == 360 else degree

    @staticmethod
    def minute_to_angle(choice: int) -> float:
        """
        Converts an minute number (0 to 60) into the angle degree in a circle

        Args:
            choice (int): Between 0 and 60 to represent the minute desired to be selected on a clock face

        Returns:
            float: The angle degree of the minute selection

        """
        if choice < 0 or choice > 60:
            raise ValueError('Out of range: please choose between a minute value between 0 and 60.  Value detected: {}'.format(choice))

        return (360 / 60) * int(choice)

    @staticmethod
    def degree_to_rad(degree):
        """
        Converts degrees into the radial value

        Args:
            degree (float): The degree value to be converted into it's radial value

        Returns:
            float: The radial value from the degree value

        """
        return degree * math.pi / 180.0

    @staticmethod
    def adjusted_angle(angle):
        """
        Adjust the angle position so we're using the top-center of the grid (12 o' clock) instead
        of right-center of the grid (3 o' clock) when we are attempting to find the appropriate
        coordinates for non-cardinal direction clock face locations

        Args:
            angle (float): The angle in degrees to be adjusted

        Returns:
            float: The adjusted angle

        """
        return 90 - (angle % 90)

    @staticmethod
    def find_quadrant(angle):
        """
        Figures out which quadrant of the x,y grid the selected hour/minute clock arm exists within

        Args:
            angle (float): The angle in degrees to the placement of the arm for the desired hour/minute

        Returns:
            int: A numerical representation of which quadrant of a grid the clock arm exists within

        """
        return int(angle / 90)

    def find_cosine(self, angle):
        hypotenuse = self.clock_face_radius()
        return int(hypotenuse * math.cos(self.degree_to_rad(self.adjusted_angle(angle))))

    def find_sine(self, angle):
        hypotenuse = self.clock_face_radius()
        return int(hypotenuse * math.sin(self.degree_to_rad(self.adjusted_angle(angle))))

    def get_selection_coords(self, angle):
        quadrant = self.find_quadrant(angle) + 1
        x = self.find_cosine(angle)
        y = self.find_sine(angle)

        quadrant_data = {
            1: {'x': x, 'y': y * -1},
            2: {'x': y, 'y': x},
            3: {'x': x * -1, 'y': y},
            4: {'x': y * -1, 'y': x * -1}
        }

        return {'x': quadrant_data[quadrant]['x'], 'y': quadrant_data[quadrant]['y']}

    def end_coords_of_angle(self, angle):
        """
        Used to convert an angle which represents a desired hour/minute selection into an x,y
        set of coordinates that can be directly clicked at within the clock face.

        Args:
            angle (int, float): The input angle for the hour/minute desired to be selected

        Returns:
            dict: The x,y coordinates of the hour/minute desired to be selected

        """
        # Figure out the clock arm length (hypotenuse) and the radian value for the hypotenuse
        hypotenuse = self.clock_face_radius()

        cardinal_coordinates = {
            angle == 90: {'x': hypotenuse + (self.clock_face.width / 2), 'y': self.clock_face.height / 2},
            angle == 180: {'x': self.clock_face.width / 2, 'y': hypotenuse + (self.clock_face.height / 2)},
            angle == 270: {'x': (self.clock_face.width / 2) - hypotenuse, 'y': self.clock_face.height / 2},
            angle == 360 or angle == 0: {'x': self.clock_face.width / 2, 'y': (self.clock_face.height / 2) - hypotenuse}
        }

        # Return our x,y coords immediately if the clock position choice or continue onto further calculations
        if True in cardinal_coordinates:
            return {'x': cardinal_coordinates[True]['x'], 'y': cardinal_coordinates[True]['y']}
        else:
            coords = self.get_selection_coords(angle)
            return {'x': coords['x'] + (self.clock_face.width / 2), 'y': coords['y'] + (self.clock_face.height / 2)}

    def time_zero_element(self):
        time_zero_element = None

        if self.hour_zero_element.exists and self.hour_zero_element.visible:
            time_zero_element = self.hour_zero_element

        if self.minute_zero_element.exists and self.minute_zero_element.visible:
            time_zero_element = self.minute_zero_element

        return time_zero_element

    def clock_face_radius(self):
        """
        Figures out what the real distance in pixels is between the center of the clock face and the center of the element which represents the 12 on a clock
        (for hours) or 00 (for minutes)

        Notes:
            Works with both 12 and 24 hour clock faces so long as you have the correct locator for the top most hour number element.

        Returns:
            int: The length of the distance form the center of the clock face to the center of the element which represents the top most time indicator (12/00)

        """
        element = self.time_zero_element()

        return int(self.clock_face.center_y_pos - element.center_y_pos)

    def set_time(self, hour, minute, meridian, save=False):
        self.click_on_hour(hour)
        self.click_on_minute(minute)

        if meridian.lower() == 'am':
            self.__asserts.becomes_interactable(self.am_element).click()
        else:
            self.__asserts.becomes_interactable(self.pm_element).click()

        if save:
            self.save()
