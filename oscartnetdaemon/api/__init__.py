import logging
from copy import copy

from oscartnetdaemon.components.argument_parser import parse_args
from oscartnetdaemon.components.launcher import Launcher
from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.configuration import Configuration
from oscartnetdaemon.core.show.item import ShowItem

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
        Components().configuration = configuration

    @staticmethod
    def configure_from_command_line() -> Configuration:
        """
        Configures the components by parsing command-line arguments and returns the configuration.

        :return: The configuration parsed from the command line.
        :rtype: Configuration
        """
        configuration = parse_args()
        if configuration.is_verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        Components().configuration = configuration

        _logger.info(f"Configuration loaded from command line arguments {configuration}")
        return configuration

    @property
    def channels_info(self) -> list[ChannelInfo]:
        if Components().fixture_updater is None:
            return list()

        return Components().fixture_updater.channels_info()

    @property
    def show_items(self) -> list[ShowItem]:
        if Components().show_store is None:
            return list()

        return Components().show_store.show.items

    def run_forever(self):
        """
        Starts the launcher in blocking mode.
        """
        self._launcher.start(blocking=True)

    def start(self):
        """
        Starts the launcher in non-blocking mode.
        """
        self._launcher.start(blocking=False)

    def stop(self):
        """
        Stops the launcher.
        """
        self._launcher.stop()
