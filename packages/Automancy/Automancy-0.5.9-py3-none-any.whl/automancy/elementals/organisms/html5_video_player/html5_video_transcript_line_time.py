from automancy.core import Elemental


class VideoTranscriptLineTime(Elemental):
    """ Container for the time for a transcript line """
    def __init__(self, locator: str, human_name: str, system_name: str):
        super().__init__(locator, human_name, system_name)
