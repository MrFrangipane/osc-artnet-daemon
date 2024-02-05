import logging
from datetime import datetime

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnet.components.osc_server.abstract import AbstractOSCServer
from oscartnet.core.components import Components

_logger = logging.getLogger(__name__)


class OSCServer(AbstractOSCServer):
    def __init__(self):
        super().__init__()
        self._dispatcher = Dispatcher()
        self._server: ThreadingOSCUDPServer = None

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

        elif address == '/encoder2':
            Components().mood.saturation = values[0]

        elif address == '/encoder3':
            Components().mood.value = values[0]
