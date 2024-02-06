import logging
import socket
import time
from threading import Thread

from oscartnetdaemon.components.fixtures_updater.concrete import FixturesUpdater
from oscartnetdaemon.components.osc_server.concrete import OSCServer
from oscartnetdaemon.components.argument_parser import parse_args
from oscartnetdaemon.core.components import Components

_logger = logging.getLogger(__name__)


class Launcher:

    def __init__(self):
        self._osc_thread: Thread = None
        self._fixture_thread: Thread = None

    def exec(self):
        #
        # Command line arguments
        arguments = parse_args()

        if arguments.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        #
        # OSC
        Components().osc = OSCServer()
        self._osc_thread: Thread = Thread(target=Components().osc.start, daemon=True)
        self._osc_thread.start()

        #
        # Artnet
        artnet_target_ip = socket.gethostbyname(arguments.artnet_target_ip)
        Components().artnet.start(
            target_node_ip=artnet_target_ip,
            universe_number=arguments.artnet_universe
        )

        #
        # Fixtures Updater
        Components().fixture_updater = FixturesUpdater()
        Components().fixture_updater.load_fixtures()
        self._fixture_thread: Thread = Thread(target=Components().fixture_updater.start, daemon=True)
        self._fixture_thread.start()

        #
        # Loop
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                _logger.info(f"Last OSC message received {Components().osc.last_message_datetime}")
                break
