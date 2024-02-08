import logging
from copy import copy

from oscartnetdaemon.components.argument_parser import parse_args
from oscartnetdaemon.components.launcher import Launcher
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.configuration import Configuration

_logger = logging.getLogger(__name__)


class OSCArtnetDaemonAPI:
    def __init__(self):
        self._launcher = Launcher()

    @property
    def artnet_universe(self):
        if Components().fixture_updater is None:
            return bytes(512)

        return copy(Components().fixture_updater.universe)

    @staticmethod
    def configure(configuration: Configuration):
        Components().configuration = configuration

    @staticmethod
    def configure_from_command_line():
        configuration = parse_args()
        if configuration.is_verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        Components().configuration = configuration

        _logger.info(f"Configuration loaded from command line arguments {configuration}")

    def run_forever(self):
        self._launcher.start(blocking=True)

    def start(self):
        self._launcher.start(blocking=False)

    def stop(self):
        self._launcher.stop()
