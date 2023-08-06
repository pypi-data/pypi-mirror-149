""" ./core/elemental.py """
from lxml.etree import XPath, XPathSyntaxError

from selenium.common.exceptions import WebDriverException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as wait
from selenium.webdriver.support.ui import WebDriverWait

from .automancy_chain import AutomancyChain
from .browser import Browser
from .external_javascript import drag_and_drop

from ..decorators import interaction


class Elemental(object):
    """ The base object for all web element type of component """
    def __init__(self, locator, human_name, system_name, uses_w3c: bool = False, **kwargs):
        """
        The base class for more specific types of elements.  This Elemental contains general
        methods that can be used by any Selenium WebElement.  Also maintains some state information
        about the element beyond what the Selenium WebElement will tell you.  Acts a proxy for
        Selenium WebElement methods to allow them to be accessible by Elementals that are specific
        to any test which extend this class.

        Args:
            locator (str): Xpath string for the lookup
            human_name (str): the human readable name of the Elemental; used for ease of log and reporting output
            system_name (str): the system-readable name of the Elemental; used for internal reference only

        """
        super().__init__()
        self.browser = Browser.find_driver()
        self.__uses_w3c = uses_w3c
        self.__browser_used = ''

        self._text = ''
        self._height = ''
        self._width = ''

        self.locator = locator
        self.name = human_name
        self.system_name = system_name
        self.x = ''
        self.y = ''

        if 'options' in kwargs:
            self.__process_options(kwargs['options'])

    @staticmethod
    def __type_error_message(other_element):
        return 'Element to compare against is not an instance of Elemental.  Received: {}'.format(type(other_element))

    def __process_options(self, options: dict) -> None:
        """
        Sets the values om options as attributes of self

        Args:
            options (dict): contains additional properties as a dictionary

        Returns:
            None

        """
        for key, value in options:
            setattr(self, key, value)

    @property
    def clickable(self):
        """ Determines if the element is clickable via Selenium """
        try:
            if WebDriverWait(self.browser, 1).until(wait.element_to_be_clickable((By.XPATH, self.locator))):
                return True

        except WebDriverException as error:
            if "A JavaScript exception occurred: Object is not a constructor" in error.msg:
                raise WebDriverException(
                    msg='Clickability Issue: Driver == {0} (If Safari, the driver is very strict on what is "clickable" or not.  Try pointing to a different element tag type (I.E, <a> or <button>, etc)'.format(
                        self.browser_used))

    @property
    def computed_styles(self) -> dict:
        """
        Gets the full list of computed styles from an element.

        Does not rely on the styles="*" html attribute.

        Executes a custom javascript command to return the values of all applied styles

        Returns:
            dict: All computed styles for an element

        """
        javascript_getter = '''
        var s = '';
        var o = getComputedStyle(arguments[0]);
        for(var i = 0; i < o.length; i++) {s+=o[i] + ':' + o.getPropertyValue(o[i])+';';} 
        return s;
        '''

        computed_styles = {}
        styles_string = self.browser.execute_script(javascript_getter, self.element())

        for style in styles_string.split(';'):
            if style:
                split_style = style.split(':')
                computed_styles[split_style[0]] = split_style[1].replace('""', '')

        return computed_styles

    @property
    def enabled(self):
        """
        Getter wrapper for the Selenium WebElement "is_enabled()" method

        Notes:
            SafariDriver handles "is_enabled()" differently and (sort of) incorrectly from other
            browser drivers.  SafariDriver appears to requires a web element to require the specific
            attribute syntax 'disabled="disabled"' (or perhaps 'disabled="true"') in order for it
            to correctly return False.  If a web element simply uses "disabled" as an attribute as
            is acceptable with Chrome, Firefox, Edge, etc, SafariDriver will incorrectly return True.

            To work around this extremely irritating plague upon the land, this method is looking for
            the 'disabled' attribute directly on the element when browser_used is Safari.

            Confidence is king.  Hail to the King!

        Returns:
            (bool): True if the element is enabled, False if not

        """
        if self.browser_used.lower() == 'safari':
            disabled_attribute = self.element().get_attribute('disabled')

            if disabled_attribute and disabled_attribute == 'true':
                return False

        return self.element().is_enabled()

    @property
    def background_css(self):
        """ Returns the string value of the CSS property 'background' """
        return self.element().value_of_css_property('background')

    @property
    def background_color_css(self):
        """ Returns the string value of the CSS property 'background-color' """
        return self.element().value_of_css_property('background-color')

    @property
    def cursor(self):
        """
        Returns the value stored within the html attribute 'cursor'.

        Notes:
            Return values can be as follows (at least, there are other lesser used values)

            '' : Element does not have the cursor attribute, considered not clickable
            'default' : Element click events will not bubble up, considered not clickable
            'pointer' : Element click events will bubble up, considered clickable

            This attribute is important for iOS devices as it is utilized for determining if
            non naturally clickable tag types (div, section, span, p, etc) will allow click
            events to bubble up to the top layer.

            cursor="pointer" allows tap/click events to happen on iOS devices, a feature that
            is controlled at the OS level so that all browsers on iOS devices must conform to
            the rule.

            cursor="default" generally means that the element cannot be clicked.

            Besides determining if an element will be properly handled on iOS devices, "cursor"
            doubles as a backup for determining if an element is enabled/disabled when methods
            and properties such as "enabled" or "clickable" cannot be used or provide false
            results.

        Returns
            str: The value of the html attribute "cursor".

        """
        cursor = ''

        cursor_attribute = self.element().get_attribute('cursor')

        if cursor_attribute:
            cursor = cursor_attribute

        return cursor

    @property
    def width(self):
        """
        Looks up the size of the object with Selenium and returns width

        Returns:
            (int) The width of the element

        """
        return self.get_size()['width']

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        """
        Looks up the size of the object with Selenium and returns height

        Returns:
            (int) The height of the element

        """
        return self.get_size()['height']

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def screen_x_pos(self):
        """ Returns the true x coordinate for the element in relationship to it's position on the screen (not just to the window) """
        # Dimension values of component
        window_x_pos = self.browser.get_window_position()['x']
        window_width = self.browser.get_window_size()['width']
        html_body_width = self.browser.find_elements(By.XPATH, '//body').rect['width']

        # The offset pixel amount from the screen for where the html body actually begins
        window_x_offset = window_width - html_body_width + window_x_pos

        # Return the exact x coordinate location of the element in relationship to the screen itself
        return window_x_offset + self.x_pos

    @property
    def screen_y_pos(self):
        """ Returns the true y coordinate for the element in relationship to it's position on the screen (not just to the window) """
        # Dimension values of component
        window_y_pos = self.browser.get_window_position()['y']
        window_height = self.browser.get_window_size()['height']
        html_body_height = self.browser.find_elements(By.XPATH, '//body').rect['height']

        # The offset pixel amount from the screen for where the html body actually begins
        window_y_offset = window_height - html_body_height + window_y_pos

        # Return the exact x coordinate location of the element in relationship to the screen itself
        return window_y_offset + self.y_pos

    @property
    def x_pos(self):
        return self.element().rect['x']

    @property
    def y_pos(self):
        return self.element().rect['y']

    @property
    def center_x_pos(self):
        """ Returns the center point x coord of the element instead of the top left """
        return int(self.x_pos + self.width / 2)

    @property
    def center_y_pos(self):
        """ Returns the center point y coord of the element instead of the top left """
        return int(self.y_pos + self.height / 2)

    def drag_to_element(self, target_element):
        """
        Executes custom javascript code which gets around drag-and-drop limitations of Selenium

        Args:
            target_element (Any): Any Automancy object desired to be dragged to

        Returns:
            None

        """
        self.browser.execute_script(drag_and_drop, self.element(), target_element.element())

    def drag_by_offset(self, x: int, y: int):
        """
        OS level mouse controls to click, hold, and drag this element by x, y offset values

        Notes:
            Similar operations to drag_to_element(...) except that providing a negative x value
            moves the element left and a negative y value will move the element up

        Args:
            x (int): The new x coordinate desired to be moved to
            y (int): The new y coordinate desired to be moved to

        Returns:
            None

        """
        self.browser.execute_script(drag_and_drop, self.element(), self.element(), x, y)

    @property
    def text(self):
        """
        Inspects the WebElement that contains the text value for the transcript line

        Returns:
            (str) The displayed text value for the line

        """
        # Text can returned by different browser drivers with unwanted characters (SafariDriver is the worst)
        # TODO -> Test this with a body of text in an element which might have multiple lines which might use \n, \r, \t
        return self.element().text.replace('\n', '').replace('\t', '').replace('\r', '').strip(' ')

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def browser_used(self):
        """ Determines which webdriver browser is being used """
        self.__browser_used = self.browser.capabilities['browserName']
        return self.__browser_used

    @browser_used.setter
    def browser_used(self, value):
        self.__browser_used = value

    @property
    def exists(self, other=''):
        """
        Sometimes you need to know if an element exists in the DOM but you don't want to
        do a WebDriverWait call; you just need something quick and dirty.  This will do it.

        Notes:
            Takes an optional parameter (other) which allows any calling object to check
            for any element by an alternate xpath.

            By default, this method will check to see if the calling objects self.locator
            xpath value exists in the DOM

        Args:
            other (str): Optional alternative xpath string to the calling objects self.locator value

        Returns:
            bool: True if at least one element exists with the locator, False if not

        """
        exists = False
        locator = self.locator

        if other:
            locator = other

        if self.valid_xpath(to_validate=locator):
            elements = self.browser.find_elements(By.XPATH, locator)

            if elements:
                exists = True

        return exists

    @property
    def visible(self):
        """
        When you want to know if the element is visible or not
        Returns:
            bool: True if the webelement has the visible attribute and value that would make it visible, False if not.

        """
        return self.element().is_displayed()

    def press_enter(self):
        """ Uses Keys.ENTER on the Selenium WebElement """
        self.element().send_keys(Keys.RETURN)

    @property
    def attributes(self) -> dict:
        return self.get_attributes()

    def get_attributes(self) -> dict:
        """

        Returns:
            dict: All all of the attributes that an element has as a key value pair

        """
        return self.browser.execute_script(
            'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
            self.element(),
        )

    def shift_click(self):
        """
        Performs a click action as if a real user were holding down the Shift key while clicking
        on an element.  Allows the selection of multiple elements/rows/etc in a list/table/etc.
        """
        AutomancyChain(self.browser).key_down(Keys.SHIFT).click(self.element()).key_up(Keys.SHIFT).perform()

    def ctrl_click(self):
        """
        Performs a click action as if a real user were holding down the CTRL key while clicking
        on an element.  Allows the selection of two or more elements/rows/etc in a list/table/etc.
        """
        AutomancyChain(self.browser).key_down(Keys.CONTROL).click(self.element()).key_up(Keys.CONTROL).perform()

    def get_coordinates(self):
        """
        Inspects the x/y position of the element

        Returns:
            (dict): Contains the x/y coordinates of the elements location in a dictionary.

        """
        coordinates = self.element().location
        self.x = coordinates['x']
        self.y = coordinates['y']
        return coordinates

    def get_size(self):
        """
        Inspects the size of the element

        Returns:
            (dict): Contains the height and values in a dictionary.

        """
        size = self.element().size
        self._height = size['height']
        self._width = size['width']
        return size

    def position_relative_to(self, other):
        """
        Checks the position of this object in relation to 'other'

        Args:
            other (Elemental): The object to compare against

        Returns:
            (str): above, below, left, right

        """
        below_or_none = 'below' if self.located_below(other) else ''
        left_or_none = 'left' if self.located_left_of(other) else ''

        vertically = 'above' if self.located_above(other) else below_or_none
        horizontally = 'right' if self.located_right_of(other) else left_or_none

        return '{0} {1}'.format(vertically, horizontally).strip(' ')

    def same_size_as(self, *args):
        if not len(args):
            return False

        this_size = self.get_size()

        this_height = this_size['height']
        this_width = this_size['width']

        # Get the height and width of each of the other objects
        other_sizes = [element.get_size() for element in args]

        for other_size in other_sizes:
            if this_height != other_size['height'] or this_width != other_size['width']:
                return False

        return True

    def located_above(self, other):
        """
        Checks to see if this object is positioned above 'other' in the DOM

        Args:
            other (Elemental): The object to compare against

        Returns:
            (bool): True if positioned above, False if not

        """
        if isinstance(other, Elemental):
            self.get_coordinates()

            if self.y < other.get_coordinates()['y']:
                return True
            else:
                return False

        else:
            raise TypeError(Elemental.__type_error_message(other))

    def located_below(self, other):
        """
        Checks to see if this object is positioned below 'other' in the DOM

        Args:
            other (Elemental): The object to compare against

        Returns:
            (bool): True if positioned below, False if not

        """
        if isinstance(other, Elemental):
            self.get_coordinates()

            if self.y > other.get_coordinates()['y']:
                return True
            else:
                return False

        else:
            raise TypeError(Elemental.__type_error_message(other))

    def located_right_of(self, other):
        """
        Checks to see if this object is positioned right of 'other' in the DOM

        Args:
            other (Elemental): The object to compare against

        Returns:
            (bool): True if positioned right of, False if not

        """
        if isinstance(other, Elemental):
            self.get_coordinates()

            if self.x > other.get_coordinates()['x']:
                return True
            else:
                return False

        else:
            raise TypeError(Elemental.__type_error_message(other))

    def located_left_of(self, other):
        """
        Checks to see if this object is positioned left of 'other' in the DOM

        Args:
            other (Elemental): The object to compare against

        Returns:
            (bool): True if positioned left of, False if not

        """
        if isinstance(other, Elemental):
            self.get_coordinates()

            if self.x < other.get_coordinates()['x']:
                return True
            else:
                return False

        else:
            raise TypeError(Elemental.__type_error_message(other))

    def duplicate(self):
        """
        Effectively creates a duplicate of the Elemental but only retaining the name and locator
        from the original

        Returns: A duplicate of this object keeping the name and locator properties.

        """
        return self.__class__(self.locator, self.name, self.system_name)

    def properties(self):
        """
        Returns the properties of this class as a dictionary without the underscores that
        normally indicate that a property is private (which they aren't but appear as if they
        are because they're sometimes created that way)
        :return:
        :rtype:
        """
        properties = {}

        for key, value in self.__dict__.items():
            if key.startswith('_'):
                properties[key.strip('_')] = value

        return properties

    def element(self, lookup_type=wait.presence_of_element_located):
        """
        This method invokes Selenium's explicit wait method which waits until an html element is available before
        assigning it to an object.
        :param lookup_type: The style of elemental search on the page (Examples: Examples: http://selenium-python.readthedocs.org/en/latest/waits.html)
        :type lookup_type:
        :return:
        """
        if self.browser:
            web_element = WebDriverWait(self.browser, 30).until(lookup_type((By.XPATH, self.locator)))
            web_element._w3c = self.__uses_w3c
            return web_element

    def find_elements(self, locator):
        """
        Allows the lookup of all elements within the Selenium WebElement when it's
        known / desired that multiple WebElements to be found.

        Examples:
            Xpath ends in //td and there are multiple <td> elements found in an xpath search.

        Args:
            locator (str): Xpath string that represents what is believed will find multiple elements

        Returns:
            List of WebElements

        """
        if self.browser:
            return self.browser.find_elements(By.XPATH, locator)

    def scroll_to(self):
        """
        Performs a javascript command to scroll the element into view.

        Returns: None

        """

        if self.browser:
            self.browser.execute_script('arguments[0].scrollIntoView({behavior: "auto", block: "center", inline: "nearest"});', self.element())

    def refresh(self):
        """
        Refreshes the browser html and waits until the presence of this WebElement is available.
        Returns the Selenium WebElement object to this object's element property.

        This method should be used in except blocks for StaleElementReferenceException encounters
        """
        self.element()

    @interaction
    def click(self):
        """
        Proxy for clicking an element but performs additional actions to wait for visibility and clickability

        Notes:
            Also attempts to detect if the element is displayed or not, and if it's not an attempt to scroll
            to the element is performed before actually clicking on it.

            The following Java code comes from stack overflow as a possible solution for how to deal with "un-clickable" elements.

            public void clickElement(WebElement el) throws InterruptedException {
                ((JavascriptExecutor) driver).executeScript("arguments[0].click();", el);
            }

        """
        try:
            if not self.visible:
                self.scroll_to()

            self.element().click()

        except WebDriverException as error:
            # Resolves issues where a permanent overlay in the DOM prevents automated interaction
            if 'Other element would receive the click' in error.msg:
                self.element().send_keys(Keys.RETURN)
            elif isinstance(error, ElementNotInteractableException):
                self.browser.execute_script('arguments[0].click()', self.element())

    @interaction
    def change_style(self, attribute, value):
        """
        Changes an elements style attribute through a javascript script execution command.

        Args:
            attribute (str): A style used by the element
            value (str): The value that you want to change the attribute to.

        Notes:
            No preemptive validation is performed for if the element has the target style
            or if it has styles associated with it at all.

        Returns:
            None

        """
        script_string = 'arguments[0].style.{attr} = "{value}";'.format(attr=attribute, value=value)
        self.browser.execute_script(script_string, self.element())

    def hover_over(self):
        """
        Proxy for hovering the mouse over an element.

        IMPORTANT:
            This method is particularly valuable when using the Firefox webdriver for
            reasons discussed in Notes.  Some click() actions will fail with Firefox
            without first hovering over the element that you want to click.

        Notes:
            AutomancyChain.move_to_element will fail in Firefox and Safari if
            you do not scroll the element on screen beforehand so detection
            of the browser environment being used is performed.

        """
        if 'firefox' in self.browser_used:
            element = self.element()
            x = element.location['x']
            y = element.location['y']
            scroll_by_coord = 'window.scrollTo({x},{y});'.format(x=x, y=y)
            scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
            self.browser.execute_script(scroll_by_coord)
            self.browser.execute_script(scroll_nav_out_of_way)
        else:
            AutomancyChain(self.browser).move_to_element(self.element()).perform()

    def is_active(self, selector):
        """
        Boolean for if the element is active on the page
        :return: Boolean if element is active
        :rtype: bool
        """

        if selector in self.classes():
            return True

        return False

    @interaction
    def styles(self):
        """
        Takes a snapshot of the state of an elements 'style' definitions.
        Useful when you want to compare the CSS changes before and after a mouse hover.
        :return: A dictionary representing a the current state of a web elements style definition.
        :rtype: dict
        """
        return dict(style.split(': ') for style in self.element().get_attribute('style').split('; '))

    @interaction
    def classes(self):
        """
        Returns the class properties that an element is using

        Returns:
            (list): The class property names.

        """
        return [class_name for class_name in self.element().get_attribute('class').split(' ')]

    @staticmethod
    def text_matches(*args):
        """
        Compares any number of strings to discover if they are the same.
        Removes all spaces from the string and causes all strings to be lowercase.
        This is done in order to ensure that the strings are homogenized.
        This functionality may change.
        :param args: Any number of strings to compare to each other
        :type args: str
        :return:
        :rtype:
        """
        compare_strings = [text.replace(' ', '').lower() for text in args]
        return len(set(compare_strings)) <= 1

    def valid_xpath(self, to_validate=''):
        """
        Check to see if an xpath is valid with a boolean return.

        Notes:
            If the optional parameter "to_validate" is not used,
            the calling objects own locator is used instead.

        Args:
            to_validate (str): A (hopefully) valid xpath when you
            don't want to use the the calling objects own locator.

        Returns:
            bool: True if the string is valid xpath, False if not.

        """
        valid = False

        try:
            if not to_validate:
                to_validate = self.locator

            valid = bool(XPath(to_validate).path)
        except XPathSyntaxError:
            pass

        return valid

    def new_tab(self):
        """ Opens a new tab for the browser """
        self.browser.execute_script('window.open("");')
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def next_tab(self):
        """
        Switches the browser context to the next tab that's open.
        Opens a tab if there is only one tab open.
        Selenium does not have a better way of handling this need.
        For now each Elemental instance will have this ability.
        """
        # Create a new tab if there is only one open
        if len(self.browser.window_handles) == 1:
            self.new_tab()
            return

        # Get the current tab's window handle
        current_handle = self.browser.current_window_handle

        # If the current handle equals the last known window handler open we want to switch to the first handle created
        if current_handle == self.browser.window_handles[-1]:
            self.browser.switch_to.window(self.browser.window_handles[0])
        else:
            next_handle = self.browser.window_handles.index(current_handle)
            self.browser.switch_to.window(self.browser.window_handles[next_handle + 1])

    def write(self, text: str):
        return NotImplementedError('Method `.write()` is not implement for this object, type: {}'.format({type(self)}))
