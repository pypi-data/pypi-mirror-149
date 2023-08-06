from automancy.core import Elemental


class GridSegment(Elemental):
    """ And object which represents a single piece of the larger grid """
    def __init__(self, locator, human_name: str, system_name: str):
        super().__init__(locator, human_name, system_name)

    def __getitem__(self, item: str):
        if not isinstance(item, str):
            raise TypeError

        if hasattr(self, item):
            return getattr(self, item)
        else:
            self[item] = Elemental('', item, item.lower().replace(' ', '_').strip())
            return getattr(self, item)

    def __setitem__(self, key, value) -> None:
        """
        Change the locator based on the grid segments specific locator so the component
        will be a hierarchical child of the segment being referenced.

        Args:
            key ():
            value ():

        Returns:
            None

        """
        if hasattr(value, 'locator') and self.locator not in value.locator:
            locator_extension = self.locator + value.locator
            value.locator = locator_extension

        setattr(self, key, value)
