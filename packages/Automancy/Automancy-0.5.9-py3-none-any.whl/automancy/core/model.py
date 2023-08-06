""" ./core/model.py """


class Model(object):
    """ Don't know yet """
    def __init__(self):
        self.__children = {}

    def add(self, elemental_class, locator: str, human_name: str, system_name: str = '', overwrite: bool = False) -> None:
        """
        Adds an Elemental based object as a child to this model

        Args:
            elemental_class (): a pointer to the class of object which will be instantiated as a child of this model
            locator (str): the segmented xpath string meant to be used as a locator for the element being added
            human_name (str): a human readable name useful in being displayed in logs or in other meaningful output
            system_name (str): OPTIONAL, a system readable name meant as an internal reference value
            overwrite (bool): OPTIONAL, acts as protection against overwriting existing components.

        Returns:
            None

        """
        if not system_name:
            system_name = human_name.lower().replace(' ', '_').strip(' ')
        else:
            if ' ' in system_name:
                raise ValueError('A custom system_name value must not include spaces or capital letters')

        # Protects against accidental overwrites if overwrite is not set to True
        if not hasattr(self, system_name) or overwrite:
            # Takes the parent locator and adds the child locator to the end of it
            concatenated_locator = getattr(self, 'locator') + locator
            setattr(self, system_name, elemental_class(concatenated_locator, human_name, system_name=system_name))
            self.__children[system_name] = getattr(self, system_name)
