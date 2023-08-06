from automancy.core import Elemental


class VideoCaptionLine(Elemental):
    """ Container for the captions that will appear over the video viewport """
    def __init__(self, locator: str, human_name: str, system_name: str):
        super().__init__(locator, human_name, system_name)
