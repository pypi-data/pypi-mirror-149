from automancy.core import Elemental


class VideoControls(Elemental):
    """ The container object for playback and volume controls """
    def __init__(self, locator: str, human_name: str, system_name: str):
        super().__init__(locator, human_name, system_name)
        self.play_button = None
        self.pause_button = None
        self.stop_button = None
        self.mute_button = None
        self.volume_button = None
        self.volume_slider = None
        self.settings_button = None
        self.captions_button = None
        self.progress_slider = None
        self.time_indicator = None
        self.full_screen_button = None
