""" ./atoms/text_input.py """
import platform

from selenium.webdriver.common.keys import Keys

from automancy.core import Elemental
from automancy.decorators import interaction


class TextInput(Elemental):
    """ Object model for a text input form element """
    def __init__(self, locator: str, human_name: str, system_name: str, text: str = ''):
        """
        Notes:
            Allows for the optional "text" parameter for storing a value that will later be used to enter form data

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            text (str): OPTIONAL, used to store the text which can later be entered into the field

        """
        super().__init__(locator, human_name, system_name)
        self.__text = text

    def __repr__(self):
        """ Direct access returns value held in self.text to make text access easier """
        return self.text

    @property
    def required(self) -> bool:
        return self.element().get_attribute('required')

    @property
    def text(self) -> str:
        """
        Override for the Elemental base class .text property because
        we don't want TextInput form elements to use the base class
        getter to override the value that we define as the input value.

        Returns:
            (str) Value to be entered into the text input form element.

        """
        return self.__text

    @text.setter
    def text(self, value: str):
        self.__text = value

    @property
    def value(self):
        """
        Proxy for Selenium's WebElement.get_attribute('value') as a class property getter.

        Used when desiring to know what the value that is already entered into an input field.

        Returns:
            (str) The value that is already entered into the input field.

        """
        return self.element().get_attribute('value')

    @property
    def placeholder(self):
        """
        Proxy for Selenium's WebElement.get_attribute('placeholder') as a class property getter.

        Returns:
            str: The text value for a text inputs' placeholder attribute

        """
        return self.element().get_attribute('placeholder')

    def clear(self):
        """
        Clears the input field of all text.

        Notes:
            Does not use the traditional element().clear() command because this command does not
            always function correctly in all situations.

            For compatibility purposes, this method selects all text with Control/Command + A to
            select all then uses the delete key to remove the text.

            Handles Mac and non-Mac environments.

        """
        # Click the input field element for good measure and focus
        self.click()

        # Use the correct key press for Mac vs non-Mac environments
        if platform.system() == 'Darwin':
            self.element().send_keys(Keys.COMMAND, 'a')
        else:
            self.element().send_keys(Keys.CONTROL, 'a')

        # With all selected, press the delete key to erase
        self.element().send_keys(Keys.DELETE)

    def entered(self) -> str:
        """ Syntactic sugar for the "value" property, was the original implementation, no need to deprecate at the time. """
        return self.value

    def update(self, text: str):
        """
        A concise and (hopefully) full-proof way of changing the text of a text input element.

        Notes:
            To help ensure that things are done properly, we're going to click on the element first,
            then perform .clear() on it which uses the Selenium .send_keys() method using the Keys
            module to select all of the text and hit the Delete key, THEN enter the new text.

            The 'text' argument isn't technically optional since there is a check for an empty string
            value for it which raises an exception, but it's been decided to keep it this way to match
            the design of TextInput.write(text='Blah blah blah') and it's syntax use.

        Args:
            text (str): A string that you wish to change the field to

        Returns:
            None

        """
        # Make sure no one tries to pull a fast one on us...
        if not isinstance(text, str):
            raise TypeError('The "text" argument must be of type str, you attempted using a {type} object'.format(type=type(text)))

        # Make sure that they're not doing anything dumb too...
        if not text:
            raise ValueError('The "text" argument cannot be an empty string.  Sorry buck-o...')

        self.click()
        self.clear()
        self.write(text=text)

    @interaction
    def write(self, text: str, clear_first: bool = True):
        """
        Writes text to the input field from the self.text property if the optional text argument isn't set.

        Notes:
            Proxy for sending keys to an element.

        Args:
            text (str): Optional, a specific string value that could be written to
            clear_first (bool): Optional, clears the input field first.  Defaults to True, allows the existing input text to be preserved before writing new text.
            the input field.

        Returns:
            None

        """
        # Clear the current form value
        if clear_first:
            self.clear()

        # Click the element just to make sure we have it selected
        self.click()

        # Enter the value after making sure the element has focus
        self.click()
        self.element().send_keys(text)
