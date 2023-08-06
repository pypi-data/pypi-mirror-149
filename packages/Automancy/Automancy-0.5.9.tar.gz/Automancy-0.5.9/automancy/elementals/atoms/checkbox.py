""" ./atoms/checkbox.py"""
from automancy.core import Elemental


class Checkbox(Elemental):
    """ Atom Elemental for checkbox DOM objects """
    def __init__(self, locator: str, human_name: str, system_name: str, check_indicator: str = ''):
        """
        Allows for the optional "check_indicator" parameter intended to do a lookup against the element to discover
        if it contains some class or other attribute which defines that the element is actually checked.

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            check_indicator (str): Optional, Xpath that can be used to discover if the element is checked

        Examples:
            if 'is-checked' in my_checkbox.classes: ...

        """
        super().__init__(locator, human_name, system_name)
        self.is_checked = False
        self.check_indicator = check_indicator

    def check(self) -> None:
        """
        Wrapper for the .click() method in Elemental

        Changes the boolean value for is_checked to True

        Returns:
            None

        """
        self.click()
        self.is_checked = True

    def uncheck(self) -> None:
        """
        Wrapper for the .click() method in Elemental

        Changes the boolean value for is_checked to False

        Returns:
            None
        """
        self.click()
        self.is_checked = False

    def checked(self, child_xpath: str = '') -> bool:
        """
        Inspects all properties of an element, searching for the check_indicator.

        If it finds it then True will be returned, False if not

        Args:
            child_xpath (str): Optional - Used when this element has a child element which actually has the attribute value stored in self.check_indicator

        Notes:
            Relies on self.check_indicator.  If not set, raises AttributeError

        Returns:
            bool: True if the check indicator string is found within any of the attributes for the element, False if not

        """
        if not self.check_indicator:
            raise AttributeError('The property "check_indicator" is not set.  This property must be set before attempting Checkbox.is_checked()')

        if child_xpath:
            child_object = Elemental(self.locator + child_xpath, '{} Child Checkbox', 'checkbox_child'.format(self.name))
            child_attrs = child_object.get_attributes()

            for value in child_attrs.values():
                if self.check_indicator in value:
                    return True

            return False

        element_attrs = self.get_attributes()
        for value in element_attrs.values():

            if self.check_indicator in value:
                return True

        return False
