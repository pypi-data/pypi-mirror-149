from automancy.core import Elemental

from .html5_video_transcript_line_text import VideoTranscriptLineText
from .html5_video_transcript_line_time import VideoTranscriptLineTime


class VideoTranscriptLine(Elemental):
    """ Container for a single transcription line """
    def __init__(self, locator: str, human_name: str, system_name: str, time_locator: str = '', text_locator: str = '', time_from_data_begin: bool = False):
        super().__init__(locator, human_name=human_name, system_name=system_name)
        self.line_text = VideoTranscriptLineText(locator + text_locator, human_name + ' Line Text', system_name + '_line_text')
        self.line_time = VideoTranscriptLineTime(locator + time_locator, human_name + ' Line Text', system_name + '_line_text')
        self.time_from_data_begin = time_from_data_begin

    @property
    def text(self):
        """
        Inspects the WebElement that contains the text value for the transcript line

        Returns:
            (str) The displayed text value for the line

        """
        self.scroll_to()
        return self.line_text.text

    @text.setter
    def text(self, value):
        self.line_text = value

    @property
    def time(self):
        """
        Inspects the WebElement that contains the time value for the transcript line

        Returns:
            (str) the displayed time value for the line

        """
        self.scroll_to()

        if self.time_from_data_begin:
            value = self.element().get_attribute('data-begin')
        else:
            value = self.line_time.text

            # Replace colon with a period where colon is used delineate minutes from seconds.
            if value and ':' in value:
                value = value.replace(':', '.')

        return value

    @time.setter
    def time(self, value):
        self.line_time = value
