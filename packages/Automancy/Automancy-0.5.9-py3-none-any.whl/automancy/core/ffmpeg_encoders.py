""" ./core/ffmpeg_encoders.py -> Handlers for simplified ffmpeg use """
import subprocess

from typing import Union


class FFMPEGEncoders(object):
    """ Handler for ffmpeg operations to simplify the process of starting encoders for Broadcaster events """
    def __init__(self, environment: str, account_id: str, event_id: str, source_input: str = '', desired_output: Union[str, list] = None, experimental_flags: str = ''):
        self.environment = environment
        self.account_id = account_id
        self.event_id = event_id
        self.experimental_flags = experimental_flags

        # "Protected" class member that holds a reference to the process object itself
        self.__process = None
        self.__command_list = []

        # Holds the input source string
        self.__source = source_input

        # A container for output destinations
        self.outputs = set()

        # Initially construct output setting if the optional_parameter is set.
        if desired_output:
            self.include_output(desired_output)

    @property
    def command(self) -> list:
        """ Gives us our process command argument list fully constructed """
        # TODO -> Construct the rest of the values from definable input on demand
        self.__command_list = [
            'ffmpeg', '-re', '-i', '{}'.format(self.source), '-c:a', 'aac',
            '-c:v', 'libx264', '-flags', '+global_header', '-f', 'tee',
            '-map', '0:v', '-map', '0:a', '{}'.format(self.construct_outputs())
        ]

        # Add experimental flags just before the output definition if there are any
        if self.experimental_flags:
            self.include_experimental_flags()

        return self.__command_list

    @property
    def source(self) -> str:
        """ The source input file or stream """
        return self.__source

    @source.setter
    def source(self, value):
        # TODO -> Add OS agnostic file existence validation
        self.__source = value

    @property
    def command_string(self) -> str:
        """
        Returns the entire command string as it would be if typed in to a terminal.

        Notes:
            Primarily used as a debugging shortcut

        """
        return ' '.join(self.command)

    def include_experimental_flags(self):
        if isinstance(self.experimental_flags, str):
            self.experimental_flags = self.experimental_flags.split(' ')

        for flag in self.experimental_flags:
            self.__command_list.insert(-1, flag)

    def include_output(self, uri: Union[str, list, set], clear=False) -> None:
        """
        Adds a destination to our output list that is constructed
        into our command structure before starting the encoder

        Notes:
            Outputs can be anything normally accepted by ffmpeg including
            rtmp and files

        Args:
            uri (str): Stream output destination, filename or stream url
            clear (bool): Optional, default False, If True the output list is emptied before adding
        """
        # If 'clear' is True, clear the output list first
        if clear:
            self.outputs = set()

        if isinstance(uri, (list, set)):
            # Type check all potential output URIs first
            for candidate in uri:
                if not isinstance(candidate, str):
                    raise TypeError('Output URI value must be a string, found -> {}'.format(type(candidate)))

            self.outputs.update(set(uri))
            return

        self.outputs.add(uri)

    def remove_output(self, uri: str) -> None:
        """ Reverse operation of include_output except only accept a single string as parameter """
        # Type check first
        if isinstance(uri, str):
            self.outputs.remove(uri)

    def construct_outputs(self) -> str:
        """ Creates the part of the command string which represents all stream outputs """
        # TODO -> Things like this should eventually be turned into class properties with defaults
        filter_header = '[f=flv]'
        final_output = list(self.outputs)[-1]

        # Construct our output definition when there are more than one output in our list
        full_string = ''
        for output in self.outputs:
            # Construct the output header with uri
            full_string += '{}{}'.format(filter_header, output)

            # If we're not on the last output listed, add the required pipe character
            if output is not final_output:
                full_string += '|'

        return full_string

    def start(self):
        """ Fire up the encoders """
        self.__process = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop(self):
        """ Stops the process for the encoders """
        self.__process.stdin.write(b'q\n')
