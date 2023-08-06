from .grid_segment import GridSegment


class GridSegments(object):
    """ A glorified dictionary to allow for specific type checking against the collection (instead of just being a dict) """
    def __init__(self):
        super().__init__()
        self.ordered_index = []

    def __setitem__(self, key, value):
        """ Create a new attribute for the instance through dictionary operation syntax and update the ordered index """
        if not isinstance(key, str):
            raise TypeError('Must provide a string as the name of a grid segment.  Provided: {0}'.format(type(key)))

        if not isinstance(value, GridSegment):
            raise TypeError('Must provide a GridSegment object as a value when adding to the GridSegments object.  Provided: {0}'.format(type(value)))

        setattr(self, key, value)
        self.ordered_index.append(key)

    def __getitem__(self, item):
        """ Retrieve an attribute from the instance through dictionary operation syntax. """
        return self.__dict__[item]

    def __delattr__(self, item):
        """ Allow delattr() for the instance and update the ordered index """
        if not isinstance(item, str):
            raise TypeError('Must provide a string for the name of the Segment you wish to delete.  Provided: {0}'.format(type(item)))

        if item not in self.__dict__.keys():
            raise KeyError('{0} not found within known Segment names. Known: {1}'.format(item, self.ordered_index))

        del(self.__dict__[item])
        self.ordered_index.remove(item)

    def __getattribute__(self, item):
        """ Retrieve an attribute for an instance through dot notation operation syntax """
        if not isinstance(item, str):
            raise TypeError('Must provide a string for the name of the Segment you wish to access.  Provided: {0}'.format(type(item)))

        return object.__getattribute__(self, item)

    def __iter__(self):
        """ Direct "in" operator to the ordered_index attribute """
        return iter(self.ordered_index)

    def __len__(self):
        """ Direct len() builtin method to the ordered_index attribute """
        return len(self.ordered_index)

    def clear(self):
        """ Removes all GridSegments object attributes from self and empties the ordered_index list """
        # Reset the ordered index list.
        self.ordered_index = []

        # Look for GridSegment objects within self and delete them.
        all_segments = [attr_name for attr_name, attr_object in self.__dict__.items() if isinstance(attr_object, GridSegment)]

        for segment in all_segments:
            del self.__dict__[segment]

    def items(self):
        """ Implementation to mimic dict.items() but returns a list ordered by self.ordered_index """
        return [(attribute, getattr(self, attribute)) for attribute in self.ordered_index if getattr(self, attribute, None)]

    def keys(self):
        """ Implementation to mimic dict.keys() but returns a list ordered by self.ordered_index """
        return [attribute for attribute in self.ordered_index if getattr(self, attribute, None)]

    def values(self):
        """ Implementation to mimic dict.values() but returns a list ordered by self.ordered_index """
        return [getattr(self, attribute) for attribute in self.ordered_index if getattr(self, attribute, None)]
