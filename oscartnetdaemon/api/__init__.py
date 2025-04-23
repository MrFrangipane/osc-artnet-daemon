import logging
from copy import copy

from oscartnetdaemon.components.argument_parser import parse_project_filepath
from oscartnetdaemon.components.launcher import Launcher
from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.configuration import Configuration
from oscartnetdaemon.core.show.item import ShowItem
from oscartnetdaemon.core.midi_tempo_info import MIDITempoInfo

_logger = logging.getLogger(__name__)


class OSCArtnetDaemonAPI:
    """
    The OSCArtnetDaemonAPI class.

    This class defines the API for the OSCArtnetDaemon.
    """

    def __init__(self):
        """
        OSCArtnetDaemonAPI instance initializer.
        """
        self._launcher = Launcher()

    @staticmethod
    def configure_from_command_line():
        """
        Configures the components by parsing command-line arguments and returns the configuration.

        :return: The configuration parsed from the command line.
        :rtype: Configuration
        """
        logging.basicConfig(level=logging.INFO)
        project_filepath = parse_project_filepath()
        OSCArtnetDaemonAPI.load_project(project_filepath)

    @property
    def artnet_universe(self):
        """
        Gets the Artnet universe.

        :return: The Artnet universe. If a fixture updater component exists, a copy of its universe is returned. Otherwise, bytes(512) is returned.
        :rtype: bytes
        """
        if Components().fixture_updater is None:
            return bytes(512)

        return copy(Components().fixture_updater.universe)

    @staticmethod
    def configure(configuration: Configuration):
        """
        Configures the components.

        :param configuration: The configuration to be set.
        :type configuration: Configuration
        """
        if configuration.is_verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        Components().configuration = configuration

    #
    # Project
    @staticmethod
    def new_project():
        Components().project_persistence.new()

    @staticmethod
    def load_project(filepath: str) -> None:
        Components().project_persistence.load(filepath)

    @staticmethod
    def save_project_as(filepath: str) -> None:
        Components().project_persistence.save_as(filepath)

    @staticmethod
    def save_project() -> str:
        return Components().project_persistence.save()

    @staticmethod
    def is_direct_save_available() -> bool:
        return Components().project_persistence.is_direct_save_available()

    @staticmethod
    def project_filepath() -> str:
        return Components().project_persistence.filepath

    @property
    def channels_info(self) -> list[ChannelInfo]:
        if Components().fixture_updater is None:
            return list()

        return Components().fixture_updater.channels_info()

    @property
    def show_items(self) -> list[ShowItem]:
        if Components().show_store is None or Components().show_store.show is None:
            return list()

        return Components().show_store.show.items

    def run_forever(self):
        """
        Starts the launcher in blocking mode.
        """
        self._launcher.start(blocking=True)

    def start(self) -> bool:
        """
        Starts the launcher in non-blocking mode.
        """
        self._launcher.start(blocking=False)
        return self._launcher.was_started

    def stop(self):
        """
        Stops the launcher.
        """
        self._launcher.stop()

    @property
    def tempo_info(self) -> MIDITempoInfo:
        if Components().midi_tempo is None:
            return MIDITempoInfo(0, 0)

        return Components().midi_tempo.info()

    @staticmethod
    def send_tap_tempo() -> None:
        if Components().midi_tempo is None:
            _logger.warning("No MIDI connection, tap not sent")
            return

        Components().midi_tempo.send_tap()
