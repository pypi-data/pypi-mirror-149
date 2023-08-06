from time import sleep

from automancy.core import Elemental

from .html5_video_caption_line import VideoCaptionLine
from .html5_video_container import VideoContainer
from .html5_video_controls import VideoControls
from .html5_video_transcript import VideoTranscript
from .html5_video_viewport import VideoViewport


class HTML5VideoPlayer(Elemental):
    """ The container object for all video related sub-objects and access point for all controls and other features """
    def __init__(self, locator: str, human_name: str, system_name: str, container_locator: str = '', viewport_locator: str = '//video', caption_line_locator: str = '', transcript_locator: str = ''):
        super().__init__(locator, human_name, system_name)

        self.container = None
        if container_locator:
            self.container = VideoContainer(self.locator + container_locator, human_name + ' Video Container', system_name + '_video_container')
            self.viewport = VideoViewport(self.locator + container_locator + viewport_locator, human_name + ' Video Viewport', system_name + '_video_viewport')

        # Captions are the text that appear over a video viewport
        self.caption = None
        if caption_line_locator:
            self.caption = VideoCaptionLine(self.locator + caption_line_locator,  human_name + ' Video Caption Line', system_name + '_video_caption_line')

        # Transcripts are components which show the full caption log, usually clickable taking you to the timestamp.
        self.transcript = None
        if transcript_locator:
            self.transcript = VideoTranscript(self.locator + transcript_locator,  human_name + ' Video Transcript Line', system_name + '_video_transcript_line')

        self._current_time = None
        self._stored_id = ''

        self.controls = VideoControls(self.locator + '', human_name + 'Video Controls', system_name + '_video_controls')
        self.settings = None
        self.length = 0.00
        self.width = 0.0
        self.height = 0.0

    @property
    def current_time(self):
        """
        Returns the current play time position that the video is in.

        Returns:
            (str) The current time that the video is at

        """
        return self.browser.execute_script('return document.getElementById("{0}").currentTime'.format(self.stored_id))

    @current_time.setter
    def current_time(self, value):
        if isinstance(value, float) or isinstance(value, int):
            value = str(value)

        if value:
            self._current_time = self.browser.execute_script('document.getElementById("{0}").currentTime={1}'.format(self.stored_id, value))
        else:
            self._current_time = '0.0'

    @property
    def id(self):
        """
        Getter for the webelement attribute "id"

        Returns:
            (str) The id of the associated webelement

        """
        return self.viewport.element().get_attribute('id')

    @property
    def stored_id(self):
        """
        Getter for a property called stored_id, which stores the
        "id" attribute of the web element.  Doubles as a setter
        if the class property doesn't exist.

        Notes:
            This is sort of a getter and setter method combined into one.

            The purpose of "stored_id" is to hold the last known value for
            the "id" attribute so that the methods performing javascript
            script execution (common to this class) don't have to do the
            expensive work of always interacting with the DOM or WebElement.

            This getter works by creating the class property "stored_id"
            if it doesn't exist, and setting it's value through the Video.id()
            method which looks up the actual web elements "id" attribute in
            real time.

            If the stored_id property already exists for an instance, it is simply
            returned to get around having to do a bunch of other work.

        Returns:
            (str) The last known value for the web elements "id" attribute

        """

        if self._stored_id == '':
            self._stored_id = self.id
            return self._stored_id

        return self._stored_id

    @stored_id.setter
    def stored_id(self, value):
        self._stored_id = value

    def play(self):
        """
        Run's the javascript command to play the video.

        Returns:
            (None) Nothing by the command
        """
        return self.browser.execute_script('document.getElementById("{id}").play();'.format(id=self.stored_id))

    def is_playing(self):
        """
        Every 0.25 seconds for 1 seconds, check to see if the current time is different than the previous checked time.

        Returns:
            (bool) True if video is playing, False if not.

        """
        seconds = 1
        slices = []

        if self.element():
            while seconds > 0:
                slices.append(self.current_time)
                sleep(0.25)
                seconds -= 0.25

        playing = False

        for index, time_slice in enumerate(slices):
            try:
                if time_slice < slices[index + 1]:
                    playing = True
            except IndexError:
                # End of list
                pass

        return playing

    def pause(self):
        """
        Pauses the video using the javascript executor

        Returns:

        """
        return self.browser.execute_script('document.getElementById("{id}").pause()'.format(id=self.stored_id))

    def is_paused(self):
        """
        Tells you if the video is paused using the javascript executor

        Returns:
            (bool) True if paused, False if not.

        """
        return self.browser.execute_script('return document.getElementById("{id}").paused'.format(id=self.stored_id))

    def volume(self, new_level=None):
        """
        Returns the current volume level or sets the volume level if "new_level" is not empty
        :param new_level: Optional parameter, if set and valid is used to change the level of the volume.
        :return:
        """
        if new_level:
            return self.browser.execute_script('document.getElementById("{id}").volume={level};'.format(id=self.stored_id, level=new_level))
        else:
            return self.browser.execute_script('return document.getElementById("{id}").volume'.format(id=self.stored_id))

    def is_muted(self):
        """ Determines if the video is muted with a javascript command """
        return self.browser.execute_script('return document.getElementById("{id}").muted'.format(id=self.stored_id))

    def reload(self):
        """ Reloads the video player with a javascript command """
        return self.browser.execute_script('document.getElementById("{id}").load();'.format(id=self.stored_id))

    def get_height(self):
        """
        Returns the true height dimension of the video itself (not the displayed width on the page) with a javascript command.

        Returns:
            (str) The height of the video.

        """
        self.height = self.browser.execute_script('document.getElementById("{id}").videoHeight;'.format(id=self.stored_id))
        return self.height

    def get_width(self):
        """
        Returns the true width dimension of the video itself (not the displayed width on the page) with a javascript command.

        Returns:
            (str) The width of the video.

        """
        self.width = self.browser.execute_script('document.getElementById("{id}").videoWidth;'.format(id=self.stored_id))
        return self.width

    def get_transcript(self):
        """
        Populates the transcript lines dictionary within the transcript object.

        Returns:
            None

        """
        if self.transcript and self.transcript.exists:
            self.transcript.get_lines()
