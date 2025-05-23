import logging
import time
from threading import Thread

from oscartnetdaemon.components.artnet_server import ArtnetServer
from oscartnetdaemon.components.discovery.discovery import Discovery
from oscartnetdaemon.components.fixtures_updater.fixtures_updater import FixturesUpdater
from oscartnetdaemon.components.midi_tempo.injector import inject_midi_tempo
from oscartnetdaemon.components.mood_store.mood_store import MoodStore
from oscartnetdaemon.components.osc.message_sender import OSCMessageSender
from oscartnetdaemon.components.osc.server import OSCServer
from oscartnetdaemon.components.pattern_store.store import PatternStore
from oscartnetdaemon.components.project_persistence.project_persistence import ProjectPersistence
from oscartnetdaemon.components.show_store.store import ShowStore
from oscartnetdaemon.core.components import Components

_logger = logging.getLogger(__name__)


class Launcher:

    def __init__(self):
        self._discovery_thread: Thread = None
        self._fixture_thread: Thread = None
        self._midi_thread: Thread = None
        self._osc_thread: Thread = None
        self.was_started = False
        self._is_running = False

        Components().show_store = ShowStore()
        Components().mood_store = MoodStore()  # let's keep stored moods between starts/restarts
        Components().pattern_store = PatternStore()
        Components().project_persistence = ProjectPersistence()

    def start(self, blocking):
        configuration = Components().configuration
        if configuration is None:
            _logger.error("Configuration not loaded, maybe no project loaded ?")
            return

        Components().show_store.reload_fixtures()

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
        # MIDI
        inject_midi_tempo()
        self._midi_thread: Thread = Thread(target=Components().midi_tempo.start, daemon=True)
        self._midi_thread.start()

        #
        # Artnet
        Components().artnet_servers = list()
        for target_node in configuration.artnet_target_nodes:
            new_server = ArtnetServer(
                target_node=target_node,
                universe_number=configuration.artnet_universe
            )
            Components().artnet_servers.append(new_server)
            new_server.start()

        #
        # Fixtures Updater
        Components().fixture_updater = FixturesUpdater()  # fixme understand how threading copies object to Thread ?
        self._fixture_thread: Thread = Thread(target=Components().fixture_updater.start, daemon=True)
        self._fixture_thread.start()

        # Discovery
        # TODO check with resolume and OSX devices on the network before restoring
        # Components().discovery = Discovery(address_mask=configuration.osc_server_address)
        # self._discovery_thread: Thread = Thread(target=Components().discovery.start, daemon=True)
        # self._discovery_thread.start()

        #
        # Loop
        if blocking:
            while True:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    break
            self.stop()

        else:
            self.was_started = True

    def stop(self):
        if self.was_started:
            Components().fixture_updater.stop()
            # Components().discovery.stop()
            Components().midi_tempo.stop()
            Components().osc_server.stop()
            for artnet_server in Components().artnet_servers:
                artnet_server.stop()
