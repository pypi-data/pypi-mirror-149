""" ./elementals/molecules/form.py """

from time import sleep
from automancy.core import AutomancyChain, Elemental


class Slider(Elemental):
    """ Handler for slider objects (E.G., video volume, video progress bar) """

    def __init__(self, locator: str, human_name: str, system_name: str, orientation: str, boundary_buffer: int = 0, position_attribute: str = ''):
        """

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            orientation (str): Either 'vertical' or 'horizontal'
            boundary_buffer (int): Optional, The total amount of padding around the slider components subtracted from the element width
            position_attribute (str): Optional, A defined value that can be used as a lookup reference to determine the current slider location value

        """
        super().__init__(locator, human_name, system_name)
        self.boundary_buffer = boundary_buffer / 2 if boundary_buffer else 0
        self.orientation = orientation
        self.position_attribute = position_attribute

    @property
    def width(self):
        """

        Returns:

        """
        return self.element().size['width']

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """

        Returns:

        """
        return self.element().size['height']

    @height.setter
    def height(self, value):
        self._height = value

    def change_value(self, desired_percent):
        """
        Uses clicks to directly change the slider current position to a new location
        (as opposed to clicking and dragging)

        Args:
            desired_percent (int): A percent value

        Returns:
            None

        """
        # Raise error if desired percent is not an integer
        if not isinstance(desired_percent, int):
            raise ValueError

        # Ensure that the desired percent is within 0 -> 100 boundaries
        desired_percent = 0 if desired_percent < 0 else desired_percent
        desired_percent = 100 if desired_percent > 100 else desired_percent

        target_offset_x, target_offset_y = self.define_offsets(desired_percent)

        if desired_percent > 50 and target_offset_x < 0:
            target_offset_x *= 1

        # Create the action chain
        actions = AutomancyChain(self.browser)
        actions.move_to_element(self.element())
        actions.move_by_offset(target_offset_x, target_offset_y)
        actions.click()

        # TODO -> Run tests that use this method (with sleep commented out), remove if possible
        # Arbitrary (maybe?) explicit sleep so unknown style transitions have a chance to draw.
        sleep(0.5)

        # Finally, perform the action chain
        actions.perform()

    def drag_to_value(self, desired_percent):
        """
        Not implemented

        Intended Design:
            1. Find the position of the current value position
            2. Find where the current position is in relationship to the total element length (in percent)
            3. Use the current position as the center from where the offset will start
            4. Determine the distance from the starting point to the new desired value (in percent)
            5. Use the action chain method "drag_and_drop" or "drag_and_drop_by_offset"

        Returns:
            None

        """
        raise NotImplementedError

    def define_offsets(self, desired_percent):
        """
        Defines the target offsets that are used to move the slider position to
        a target location.

        Determine proper offset values depending on if the slider is horizontal or vertical

        Returns:
            (tuple): The X and Y coordinates for the target coordinates

        """
        target_offset_x = self.get_target_offset(desired_percent) if self.orientation == 'horizontal' else 0
        target_offset_y = self.get_target_offset(desired_percent) if self.orientation == 'vertical' else 0

        return target_offset_x, target_offset_y

    def get_target_offset(self, desired_percent):
        """
        Acquires the offset value needed to move the slider to a new position
        by clicking or clicking and dragging.

        Returns:
            (int): The offset to move the slider position to.

        """
        # TODO -> Need to include sliders that are vertical
        # Store the width so we're not doing the lookup twice
        width = self.width

        # Determine the percentage slice size and the location of the middle of the slider element
        slider_percent = width / 100
        slider_middle = width / 2

        # Find the absolute target percentage that we're aiming for
        target_pixel = int(round(desired_percent * slider_percent))

        # Determine the offset from the middle of the element to target
        target_offset = max(slider_middle, target_pixel) - min(slider_middle, target_pixel)

        # Change the target offset to a negative number if it's less than half of the size of the element width
        if target_pixel < slider_middle:
            target_offset = target_offset * -1

        # Define the modifier value to compensate for element margins/padding/etc
        boundary_modifier = round(self.boundary_buffer / 2)

        # GeckoDriver is weird with how it calculates element center points when an element has margins/padding/etc.
        # Dividing the boundary modifier in half solves this.  (Haven't found an answer to why yet)
        if self.browser_used == 'firefox':
            boundary_modifier /= 2

        # Adjust the final target offset value by the boundary buffer amount.
        if desired_percent >= 50:
            target_offset += boundary_modifier
        else:
            target_offset -= boundary_modifier

        return target_offset

    def current_position(self):
        """
        Inspects the element for a determinable current slider "notch" position.
        This method uses self.position_attribute which could be something like
        the "aria-valuenow" attribute on an element.

        Returns:
            (int) The value of the slider current position indicator

        """
        if self.position_attribute:
            position_value = self.element().get_attribute(self.position_attribute)

            # Prevent situations where the query happens too fast
            while self.element().get_attribute(self.position_attribute) == 'NaN':
                position_value = self.element().get_attribute(self.position_attribute)

            return int(float(position_value))

        else:
            return None
