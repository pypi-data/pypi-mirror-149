from automancy.core import Elemental


class VideoContainer(Elemental):
    """ The container objects for surrounding element which holds a VideoViewport plus other elements """
    def __init__(self, locator: str, human_name: str, system_name: str):
        super().__init__(locator, human_name, system_name)
        self.width = 0.0
        self.height = 0.0
