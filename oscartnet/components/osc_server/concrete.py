import logging
from datetime import datetime

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnet.components.osc_server.abstract import AbstractOSCServer
from oscartnet.components.osc_server.mood_updater import MoodUpdater

_logger = logging.getLogger(__name__)


class OSCServer(AbstractOSCServer):
    def __init__(self, host=None, port=None):
        super().__init__(host, port)
        self._dispatcher = Dispatcher()
        self._server: ThreadingOSCUDPServer = None
        self._mood_updater = MoodUpdater()

    def start(self):
        _logger.info(f"Starting OSC server (host={self.host}, port={self.port})")

        self._server = ThreadingOSCUDPServer(
            server_address=(self.host, self.port),
            dispatcher=self._dispatcher
        )
        self._server.dispatcher.set_default_handler(self._handle)
        self._server.serve_forever()

    def _handle(self, address, *values):
        _logger.debug(f"{address} {values}")
        self.last_message_datetime = datetime.now()

        self._mood_updater.update(address, values)
