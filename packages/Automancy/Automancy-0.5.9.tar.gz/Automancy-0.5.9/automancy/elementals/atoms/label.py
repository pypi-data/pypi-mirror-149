""" Implementation of the Label class """
from automancy.core import Elemental


class Label(Elemental):
    """
    Representation object model for any element which contains immutable text (a label)

    Notes:
        Does not include the ability to change the text inside of the element

        Direct access to a Label object will return the text in the element with the __repr__ magic
        method (representation).  Same functionality when using "()" to call the class instance.
    """
    def __init__(self, locator: str, human_name: str, system_name: str):
        """
        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
        """
        super().__init__(locator, human_name, system_name)

    def __call__(self) -> str:
        """ Calling the Label instance directly returns the text in the element """
        return self.text

    def __repr__(self) -> str:
        """ Returns the text displayed within the element as a representation of the Label instance """
        return self.text
