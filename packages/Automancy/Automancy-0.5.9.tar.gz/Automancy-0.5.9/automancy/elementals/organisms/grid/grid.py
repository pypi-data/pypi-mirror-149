""" ./elementals/organisms/grid/grid.py """
from selenium.webdriver.common.by import By

from automancy.core import Elemental
from .grid_segment import GridSegment
from .grid_segments import GridSegments


# The Grid, a digital frontier.  I tried to picture cluster of information as they moved through
# the computer.  What did they look like?  Ships?  Motorcycles?  Were the circuits like freeways?
# I kept dreaming of a world that I'd never see.  And then, one day... I got in.
class Grid(Elemental):
    """ A collection of objects that make up a grid as seen by the user """
    def __init__(self, locator, human_name, system_name, segment_locator=''):
        """
        Notes:
            Grid.segment_components is designed to hold additional properties which exist in each
            and all grid segment held within Grid.segments at a minimum.  These components are
            intended to be a name and Elemental based object.

        Args:
            locator (str): xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            segment_locator (str): optional, xpath extension to be able to look for grid segments.

        """
        Elemental.__init__(self, locator, human_name, system_name)
        self.segments = GridSegments()
        self.segments_locator = locator + segment_locator
        self.segment_components = {}

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise TypeError

        if item in self.segments.keys():
            return self.segments[item]
        else:
            return None

    def __setitem__(self, name, locator):
        """
        Creates a new segment, adds existing desired segment_components, and adds
        the new segment to the Grid.segments dictionary.

        Args:
            name (str): Same as Elemental "name"
            locator (str): Same as Elemental "locator"

        """
        system_name = name.lower().replace(' ', '_').strip(' ')
        new_segment = GridSegment(locator, name, system_name)
        self.add_components(segment=new_segment)
        self.segments[name] = new_segment

    def __iter__(self):
        # Update the internal list of segments with the most up to date to return
        self.find_segments()
        return iter(self.segments.items())

    def __len__(self):
        return len(self.segments)

    def segment_count(self):
        """ Returns the number of segments in the grid """
        return len(self.find_segments())

    def new_segment(self, name='', locator=''):
        """
        Adds a new segment to the grid using only the name and locator
        that would be used to construct a Elemental based object.
        """
        new_name = name
        new_locator = locator

        if not new_name:
            new_name = self.next_segment_name()

        if not new_locator:
            new_locator = self.next_segment_locator()

        if new_name not in self.segments.keys():
            self[new_name] = new_locator

    def next_segment_name(self, index=None):
        """
        Generates the next segment name based on the number of existing segments.

        Args:
            index (int): Optional value to iterate the segment name value.

        Returns:
            str: "SegmentX" where X is the number of existing segments + 1

        """
        new_index = index

        if not new_index or type(index) is not int:
            new_index = len(self) + 1

        return 'Segment{0}'.format(new_index)

    def next_segment_locator(self, index=None):
        """
        Generates the next locator for a segment that's being added to Grid.segments

        Args:
            index (int): Optional value to iterate the segment name value.

        Notes:
            This is only meant to be used when creating a new segment

        Returns:
            str: '//div[@class="row"][X]' where X is the number of existing segments + 1

        """
        new_index = index

        if not new_index or type(index) is not int:
            new_index = len(self) + 1

        return self.segments_locator + '[{0}]'.format(new_index)

    def _add_components_to_segment(self, payload):
        """ Adds each of the components known in Grid.segment_components to a segment """
        segment = payload['segment']

        for component in self.segment_components.values():
            extended_locator = segment.locator + component.locator
            setattr(segment, component.name, component.duplicate())
            segment[component.name].locator = extended_locator

    def _add_component_to_segments(self, payload):
        """ Adds an attribute to each existing segments known in the instances Grid.segments property """
        component = payload['component']

        for segment in self.segments.values():
            extended_locator = segment.locator + component.locator
            setattr(segment, component.name, component.duplicate())
            segment[component.name].locator = extended_locator

    @staticmethod
    def _add_component_to_segment(payload):
        """ Adds each of the components known in Grid.segment_components to a segment """
        segment = payload['segment']
        component = payload['component']

        extended_locator = segment.locator + component.locator
        setattr(segment, component.name, component.duplicate())
        segment[component.name].locator = extended_locator

    def _add_components_to_segments(self, _):
        """ Adds components known in Grid.segment_components to all known segments """
        for component in self.segment_components.values():
            for segment in self.segments.values():
                extended_locator = segment.locator + component.locator
                setattr(segment, component.name, component.duplicate())
                segment[component.name].locator = extended_locator

    def add_components(self, **kwargs):
        """
        Adds component(s) to segment(s) as object attributes in multiple ways

        The default behavior is for all known components to be added to all known segments, overwriting by default.

        Notes:
            Depending on how you use the arguments, you can do one of four things

            1. Add all components in Grid.segment_components to all segments
            2. Add one component to all segments
            3. Add all components in Grid.segment_components to one segment
            4. Add one component to one segment.

            Example:
                1. If the argument "segment" is not None and "component" is None, all components will be added to that segment.
                2. if the argument "segment is None and "component" is not None, only that component will be added to all segments.

        """
        payload = {'segment': None, 'component': None}
        segment = False
        component = False

        if 'segment' in kwargs:
            segment = True
            payload['segment'] = kwargs['segment']

        if 'component' in kwargs:
            component = True
            payload['component'] = kwargs['component']

        pathways = {
            (True, False): self._add_components_to_segment,
            (False, True): self._add_component_to_segments,
            (True, True): self._add_component_to_segment,
            (False, False): self._add_components_to_segments
        }

        pathways[(segment, component)](payload)

    def find_segments(self):
        """
        Reads the Grid object element, searching for segments based on the segment_locator.

        Resets the Grid instances segments dictionary making this an entirely clean read of segments.

        Adds the found grid segments to the segments dictionary.
        """
        if self.segments_locator:

            # Clear to get a fresh read first
            self.segments.clear()
            segment_elements = self.find_elements(self.segments_locator)

            for _ in segment_elements:
                self.new_segment()

            return self.segments.values()

    def segments_exist(self):
        """
        Uses the Grid.segments_locator property to find out if any segment elements
        exist in the DOM

        Returns:
            bool: True if caption segments are detected, False if not

        """
        return self.browser.find_elements(By.XPATH, self.segments_locator)

    def include(self, elemental, overwrite=False):
        """
        Adds a Elemental to the Grid's segment_components dictionary.

        Notes:
            The segment_components property is a container that holds objects
            that can be added as instance properties of each segment.

        Args:
            elemental (Elemental, Dropdown): The object that is being added as a component
            overwrite (bool): Optional, acts as protection against overwriting existing components.

        """
        if elemental.name not in self.segment_components.keys() or overwrite:
            self.segment_components[elemental.name] = elemental
