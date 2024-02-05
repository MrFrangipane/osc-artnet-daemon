import logging
import sys
import time
from threading import Thread

from oscartnet.components.fixtures_updater.concrete import FixturesUpdater
from oscartnet.components.osc_server.concrete import OSCServer
from oscartnet.core.components import Components

_logger = logging.getLogger(__name__)


class Launcher:

    def __init__(self):
        self._osc_thread: Thread = None
        self._fixture_thread: Thread = None

    def exec(self):
        if "-v" in sys.argv:
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
        Components().artnet.start("127.0.0.1", 0)

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
                _logger.info("Keyboard Interrupt")
                _logger.info(f"Last OSC message received {Components().osc.last_message_datetime}")
                break
