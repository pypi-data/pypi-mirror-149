import os

from automancy.core import Elemental
from automancy.decorators.interaction import interaction


class FileInput(Elemental):
    """ Atomic Elemental for form input web elements for files """
    def __init__(self, locator: str, human_name: str, system_name: str, file_location: str = ''):
        """
        Allows for the optional "file_location" parameter for storing a path to a file being submitted

        Args:
            locator (str): Xpath string for the lookup
            human_name (str): human-readable name
            system_name (str): system-readable name
            file_location (str): Optional, represents the directory path to the file being submitted, but not to the file directly

        """
        super().__init__(locator, human_name, system_name)
        self._file = file_location
        self._text = ''

    @property
    def file(self) -> str:
        """ Returns the entire path to the file """
        return self._file

    @file.setter
    def file(self, value: str) -> None:
        if value and not os.path.isfile(value):
            raise FileNotFoundError('Could not find the file using supplied input ({0})'.format(value))

        self._file = value

    @property
    def filename(self) -> str:
        """ Returns only the name of the file without the path """
        return os.path.basename(self.file)

    @property
    def filepath(self) -> str:
        """ Returns only the path to the file without the filename """
        return os.path.dirname(self.file)

    @property
    def text(self) -> str:
        """ Proxy for self.file if self.text is not set """
        if not self._text:
            return self.file

        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @interaction
    def write(self, text: str = '') -> None:
        """
        Writes text to the input field from the self.file property if the optional
        text argument isn't set.

        Notes:
            Proxy for sending keys to an element.

        Args:
            text (str): Optional, a specific string value that could be written to
            the input field if you don't want to use the default stored file path.

        Returns:
            None

        """
        if not text:
            text = self.file

        self.element().send_keys(text)
