""" ./elementals/organisms/dropdown/dropdown.py """
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as wait
from selenium.webdriver.support.ui import Select, WebDriverWait

from automancy.elementals.atoms import Label
from automancy.core import Elemental

from .dropdown_options import DropdownOptions


class Dropdown(Elemental):
    """ Represents a dropdown based element """
    def __init__(self, locator, human_name, system_name, options=DropdownOptions()):
        """

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            options (DropdownOptions): "Options" object which simplifies the instantiation of a Dropdown object

        Notes:
            For details about the 'options' argument, see the "Notes" section in the constructor definition
            of the DropdownOptions class

        """
        super().__init__(locator, human_name, system_name)

        if not isinstance(options, DropdownOptions):
            raise TypeError('The value for the parameter "options" must be an instance of DropdownOptions, found: {}'.format(type(options)))

        # The container for the element id's for each of the drop down options
        # We want to store the ID's instead of the WebElement objects because
        # the Selenium WebElements often go stale and storing the obfuscated ID's
        # allows for the elements to be looked up at any time more freely.
        self.option_ids = []

        # The container for options that can be iterated over to be selected or clicked
        self.options = {}

        # The xpath that will loop up all options within the dropdown
        self.options_locator = options.option_locator

        # An optional xpath extension that can be concatenated at the end of an ID lookup
        # for each of the option rows within the dropdown.
        # This xpath extension is used to located an element on a per row basis that can be
        # clicked or selected (e.g, a checkbox, link, etc)
        self.option_selector_extension = options.option_selector_extension

        # Same general idea as "option_selector_extension", this property is meant to be
        # concatenated to an ID based xpath search in order to find the label that is
        # associated with each option row within a dropdown.
        # In some cases, you may want to look up / choose an option before selecting it
        # based on the text of the label visible as it is to the end user.
        self.option_label_extension = options.option_label_extension

        self.options_type = options.option_type
        self.static_options = options.static_options
        self.disconnected_options = options.disconnected_options

    def open(self, get_options=False):
        """
        Opens the dropdown menu.  By default, inspects the element for available options.

        Args:
            get_options (bool): Optional (default: False), You might want the dropdown to be inspected for available options even when static_options is True.

        Returns:
            None

        """
        self.click()

        # By default, look up the option available in the dropdown.
        if not self.static_options or get_options:
            self.get_options()

    def close(self):
        """
        Closes the dropdown by using the escape key.

        Notes:
            Uses the escape key as input in order to close the dropdown because
            trying to select the dropdown to to click it again isn't easy/possible.

            IMPORTANT: SafariDriver handles switching to the active element differently
            than other drivers (I.E, ChromeDriver and GeckoDriver) such that if the
            command driver.switch_to.active_element is used, Safari experiences issues
            interacting with other elements after the fact.

            The last point appears to be connected to switching to the active element
            after clicking a checkbox if the driver is already within a child iframe.
            (Needs further testing to be exactly sure)

            Simply using send_keys(Keys.ESCAPE) with SafariDriver doesn't have any issues however,
            with ChromeDriver (for example), if you don't use driver.switch_to.active_element before
            using send_keys(Keys.Escape), things fall apart.

            A simple try except block for an "ElementNotInteractableException" isn't good enough
            here (tested).  Without a specific switch for 'Safari' there are too many unknowable
            situations that fail.  Besides, the need for the logic switch only came about due to
            SafariDriver (and no other) requiring a special rule.

            I know, I know, I hate it too.  It feel super hacky but I've tested several more
            generic ways of handling this but this really does seem to be a Safari only concern.
            Either SafariDriver needs to be fixed (likely) or the other drivers needs to conform
            to some standard that they're not currently (unlikely).

            Examples:
                Dropdown is opened with Dropdown.open() -> options are dynamically discovered ->
                Options are checkbox based -> Checkbox is selected for the targeted option ->
                Dropdown.close() is performed -> driver.switch_to.parent_content is used to move
                up from a child iframe/context -> elements within the parent context fail to be
                interacted with inexplicably.

        Returns:
            None

        """
        if self.browser_used == 'Safari':
            self.element().send_keys(Keys.ESCAPE)
        else:
            element = self.browser.switch_to.active_element
            element.send_keys(Keys.ESCAPE)

    def deselect_all(self):
        """
        Use if you want to make sure all selectable elements in the dropdown
        are unselected before proceeding with some sequence of events.

        Returns:
            None

        """
        if not self.options:
            self.get_options()

        for option in self.options.values():
            if 'checkboxTrue' in option.classes():
                option.click()

    def get_options(self):
        """
        Inspects the dropdowns' internal elements to discover which options exist based
        on the options row locator.

        Notes:
            Current implementation is only designed to work with dropdowns that have a
            selectable element (i.e., Checkbox) and a corresponding label for that element.

        Returns:
            None

        """
        if not self.disconnected_options:
            row_locator = self.locator + self.options_locator
        else:
            row_locator = self.options_locator

        option_rows = WebDriverWait(self.browser, 30).until(wait.presence_of_all_elements_located((By.XPATH, row_locator)))

        for index, option in enumerate(option_rows, start=1):

            # Define the option locator and the Automancy object that will eventually be added to the options dictionary.
            option_locator = '{base_path}[{index}]{selector_ext}'.format(base_path=row_locator, index=index, selector_ext=self.option_selector_extension)
            new_option = self.options_type(option_locator, name='')

            try:
                # This first check is to see if the element actually exists or not.
                # The Firefox webdriver acts really weird sometimes and will find an extra element that doesn't exist.
                if self.browser.find_elements(By.XPATH, option_locator):
                    # NOTE: Dropdowns which have complex sets of options which don't conform to W3C standards should skip the wait for visibility step.
                    #       In real world experiments, dropdowns with disconnected options have issues with visibility since not all options are always loaded in).
                    # if not self.disconnected_options:
                    #    Now wait for the element to gain existence and visibility.
                    #    assertGainsExistence(new_option)
                    #    assertGainsVisibility(new_option)

                    # If the dropdown object has the option_label_extension defined, we need to target that object for the option name to be stored as the key.
                    if self.option_label_extension:
                        option_label_locator = '{base_path}[{index}]{selector_ext}'.format(base_path=row_locator, index=index, selector_ext=self.option_label_extension)
                        option_label = Label(option_label_locator, 'Option Label', 'option_label')
                        new_option.name = option_label.text
                        del option_label
                    else:
                        # Add the text from the element to the name of the option object.
                        new_option.name = new_option.text

                    # Add the new option to the dictionary of options for this dropdown.
                    self.options[new_option.name] = new_option

            except NoSuchElementException:
                # This exception handling is for situations where different browser drivers unexpectedly handle
                # presence_of_all_elements_located by finding non-existent element.  Firefox sometimes acts in
                # this way verses the Chrome webdriver.  No hypothesis exists for why this occurs at this time
                # so we're putting blind handling here to prevent edge case false negatives from stopping tests.
                pass

    def include(self, elemental):
        """
        Adds a Elemental to the Dropdowns' options dictionary.  A KeyError is raised if an option with an
        existing name is attempting to be included.

        Notes:
            This is derivative of the Grid class method "include(...)".  The difference is that
            the user needs to take special care when defining the option xpath locator and the
            option name since there is not any special magic to do the work of ensuring that
            things are done properly implicitly.  Using Dropdown.include(...) is completely manual.

        Args:
            elemental (Elemental): The object that is being added as a component

        """
        # If an option of the same name already exists, exclude it from the list of options.
        if elemental.name in self.options.keys():
            self.exclude(elemental.name)

        # Check that the new option locator doesn't already include the base dropdown locator as a substring and that they aren't the same.
        # (This would indicate that the user is attempting to use the base object xpath and the option xpath, which is fine, just keep swimming)
        if self.locator not in elemental.locator and self.locator != elemental.locator:
            # An empty or other negative value use the pre-defined options locator xpath.  If not, go ahead and use what we get.
            if not elemental.locator:
                # Since we're not collecting options on the fly we need to use the name of the object as an xpath contains text lookup
                elemental.locator = self.locator + '//*[contains(text(), "{0}")]'.format(elemental.name)
            else:
                if not self.disconnected_options:
                    elemental.locator = self.locator + elemental.locator

        # Add the new option to the options dictionary, overwriting whatever exists by design (might changes this later)
        self.options[elemental.name] = elemental

    def exclude(self, option_name):
        """
        Removes a dropdown option by name.

        Args:
            option_name (str): The name of the option wished to be removed.

        Returns:
            None

        """
        if option_name in self.options.keys():
            self.options.pop(option_name)
        else:
            raise KeyError('Option named "{0}" not found, cannot exclude from options'.format(option_name))

    def select(self, option):
        """
        A direct way of selecting an option stored within a dropdown instance.  Opens the dropdown menu if
        the option isn't visible.

        Notes:
            This method is designed to select by visible text when the dropdown object is a <select> element.

            If the option isn't visible or if the option string doesn't exist in self.options (yet), open the
            dropdown in order to trigger the options to become visible and also for the self.options dict to be
            populated with values.

        Args:
            option (str): The visible text for the option that you want to select.

        Returns:
            None

        """
        # Inspect the dropdown locator trying to determine if the dropdown is a <select> element.
        if 'select' in self.locator:
            select = Select(self.element())
            select.select_by_visible_text(option)
        else:
            try:
                # Check to see if the desired option exists at this time.  If not, open the dropdown.
                if not self.options[option].exists:
                    self.open()

                # Once open if the option is visible click it -OR- if the option happened to exist but not be visible, open the dropdown.
                if self.options[option].visible:
                    self.options[option].click()
                else:
                    self.open()

            except KeyError:
                # Also open the dropdown if the key isn't known to exist (yet... usually because it hasn't been opened before)
                self.open()

            # TODO -> Re-implement when Safari testing can be performed again
            # Safari Sucks
            # if not self.browser_used == 'Safari':
            #     assertGainsClickability(self.options[option])

            # Select the option by it's name through __getitem__
            # TODO -> Remove commented out line if dropdowns in Safari don't have a problem with it removed.
            # assertBecomesIncludedIn(option, list(self.options.keys()))
            self.options[option].click()

        self.close()

    def select_options(self, desired_options):
        """
        Selects the options that are desired based on the string that should match them.

        Args:
            desired_options (list): A list of the names of the options that you want to select

        Returns:
            None

        """
        for option in desired_options:
            if option in self.options:
                self.select(option)
