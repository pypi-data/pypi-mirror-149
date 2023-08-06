from automancy.core import Elemental


class VideoViewport(Elemental):
    """ The container object for the video feed itself """
    def __init__(self, locator: str, human_name: str, system_name: str):
        super().__init__(locator, human_name, system_name)
