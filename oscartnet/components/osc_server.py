import logging
from datetime import datetime

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnet.core.components import Components

_logger = logging.getLogger(__name__)


class OSCServer:

    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 8000

    def __init__(self):
        self.host = self.DEFAULT_HOST
        self.port = self.DEFAULT_PORT

        self._dispatcher = Dispatcher()
        self._server: ThreadingOSCUDPServer = None

        self.last_message_datetime = None

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

        if address == '/encoder1':
            Components().mood.hue = values[0]
