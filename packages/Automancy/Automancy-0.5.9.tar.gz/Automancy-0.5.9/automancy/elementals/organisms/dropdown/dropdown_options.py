""" ./elementals/organisms/dropdown/dropdown_options.py """
from automancy.core import Elemental


class DropdownOptions(object):
    """ Container for the options that a Dropdown object will use for it's operations. """
    def __init__(self, **kwargs):
        """

        Keyword Args:
            option_locator (str): Xpath string that is used to look up each of the option rows within the dropdown.
            option_type (Elemental): A reference to the Elemental class
            static_options (bool): Optional (default False), If True, get_options() will not be used on .open() if the options dictionary is not empty
            disconnected_options (bool): Optional (default False), If True, the dropdowns' option rows are not xpath children of the dropdown itself (See Notes)
            option_selector_extension (str): Optional (default ''), An additional xpath for situations in which a dropdown option uses a checkbox or something for selection.

        Notes:
            Sometimes you're working with truly horrific UI architecture, legacy components from the mid 90's perhaps.
            The parameter "disconnected_options" is for this..  It's a simple boolean flag that allows for a logic
            modification when "self.get_options()" is used.  The difference in logic is that the option_locator is
            treated as a separate xpath and not concatenated onto the Dropdowns' locator property.

            The use-case is when the children of a Dropdown (the elements that appear visually inside of a drop down menu),
            aren't actually children of the dropdown element in the DOM (they use an entirely independent xpath)

            Before you ask, yes, I've seen this in real life.  That's why the feature exists...  *grumbles*

        """
        self.option_locator = kwargs['option_locator'] if 'option_locator' in kwargs else ''
        self.option_type = kwargs['option_type'] if 'option_type' in kwargs else Elemental
        self.static_options = kwargs['static_options'] if 'static_options' in kwargs else False
        self.disconnected_options = kwargs['disconnected_options'] if 'disconnected_options' in kwargs else False
        self.option_selector_extension = kwargs['option_selector_extension'] if 'option_selector_extension' in kwargs else ''
        self.option_label_extension = kwargs['option_label_extension'] if 'option_label_extension' in kwargs else ''
