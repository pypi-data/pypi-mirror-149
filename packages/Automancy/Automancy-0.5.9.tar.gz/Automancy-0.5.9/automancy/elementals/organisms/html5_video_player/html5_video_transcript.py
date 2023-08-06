import webvtt

from automancy.core import Elemental

from .html5_video_transcript_line import VideoTranscriptLine


class VideoTranscript(Elemental):
    """ Container for caption/transcription elements and controls """
    def __init__(self, locator: str, human_name: str, system_name: str, line_locator: str = '', selector_locator: str = '', line_time_locator: str = '', line_text_locator: str = ''):
        super().__init__(locator, human_name, system_name)
        self.line_locator = self.locator + line_locator
        self.selector_locator = self.locator + selector_locator
        self.line_time_locator = line_time_locator
        self.line_text_locator = line_text_locator
        self.time_from_data_begin = False

        # Line elements should be dictionaries that look like this {'time': 0.00, 'text': ''}
        self.lines = []

        # Selection key/values should look something like 'english': '//option' ( <- xpath )
        self.selections = {}
        self.transcript_file = None

    def get_lines(self):
        """ Actively populates the Transcript.lines object with the text and time """
        lines = []

        if self.line_locator:
            line_elements = self.find_elements(self.line_locator)

            for index, line in enumerate(line_elements, start=1):

                human_name = 'Line {}'.format(index)
                system_name = 'line_{}'.format(index)
                specific_line_locator = '{0}[{1}]'.format(self.line_locator, index)

                # Construct the actual transcript line object
                line_object = VideoTranscriptLine(
                    specific_line_locator,
                    human_name,
                    system_name,
                    text_locator=self.line_text_locator,
                    time_locator=self.line_time_locator,
                    time_from_data_begin=self.time_from_data_begin
                )

                line_object.scroll_to()

                # Get the content data of the line and append it to lines[]
                lines.append(line_object)

        self.lines = lines

    def read_from_file(self, file_path):
        """
        Processes the contents of a VTT file and stores the output in
        VideoTranscript.transcript_file.

        Args:
            file_path (str): The path to the file the target VTT file

        """
        self.transcript_file = webvtt.read(file_path)

    def text_matches_file(self, file_path):
        """
        Compares the transcript line text against a source webvtt file.

        Notes:
            VideoTranscript.get_line() will be called if VideoTranscript.lines
            is empty

        Args:
            file_path (str): The path to the file the target VTT file

        """
        lines_match = []

        transcript_file = webvtt.read(file_path)

        for from_web, from_file in zip(self.lines, transcript_file.captions):
            lines_match.append(True if from_web.text == from_file.text else False)

        return False if False in lines_match else True

    def time_matches_file(self, file_path):
        """
        Compares the transcript line times against a source webvtt file.

        Notes:
            VideoTranscript.get_line() will be called if VideoTranscript.lines
            is empty

        Args:
            file_path (str): The path to the file the target VTT file

        """
        lines_match = []

        transcript_file = webvtt.read(file_path)

        for from_web, from_file in zip(self.lines, transcript_file.captions):
            lines_match.append(True if float(from_web.time) == from_file.start_in_seconds else False)

        return False if False in lines_match else True
