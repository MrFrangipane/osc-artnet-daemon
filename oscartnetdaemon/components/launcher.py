import logging
import time
from threading import Thread

from oscartnetdaemon.components.discovery.discovery import Discovery
from oscartnetdaemon.components.fixtures_updater.fixtures_updater import FixturesUpdater
from oscartnetdaemon.components.mood_store.mood_store import MoodStore
from oscartnetdaemon.components.osc.message_sender import OSCMessageSender
from oscartnetdaemon.components.osc.server import OSCServer
from oscartnetdaemon.components.artnet_server import ArtnetServer
from oscartnetdaemon.core.components import Components

_logger = logging.getLogger(__name__)


class Launcher:

    def __init__(self):
        self._discovery_thread: Thread = None
        self._fixture_thread: Thread = None
        self._osc_thread: Thread = None

    def start(self, blocking) -> None:
        configuration = Components().configuration

        #
        # Mood Store
        Components().mood_store = MoodStore()

        #
        # OSC
        Components().osc_message_sender = OSCMessageSender()

        Components().osc_server = OSCServer(
            address=configuration.osc_server_address,
            port=configuration.osc_server_port
        )
        self._osc_thread: Thread = Thread(target=Components().osc_server.start, daemon=True)
        self._osc_thread.start()

        #
        # Artnet
        Components().artnet = ArtnetServer(
            target_node_ip=configuration.artnet_target_node_ip,
            universe_number=configuration.artnet_universe
        )
        Components().artnet.start()

        #
        # Fixtures Updater
        Components().fixture_updater = FixturesUpdater()
        Components().fixture_updater.load_fixtures()
        self._fixture_thread: Thread = Thread(target=Components().fixture_updater.start, daemon=True)
        self._fixture_thread.start()

        # Discovery
        Components().discovery = Discovery(address_mask=configuration.osc_server_address)
        self._discovery_thread: Thread = Thread(target=Components().discovery.start, daemon=True)
        self._discovery_thread.start()

        #
        # Loop
        if blocking:
            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    break

            self.stop()

    @staticmethod
    def stop():
        Components().fixture_updater.stop()
        Components().discovery.stop()
        Components().osc_server.stop()
        Components().artnet.stop()
