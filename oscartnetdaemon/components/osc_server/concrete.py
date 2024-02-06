import logging
from datetime import datetime

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnetdaemon.components.osc_server.abstract import AbstractOSCServer
from oscartnetdaemon.components.osc_server.message_handler import MessageHandler

_logger = logging.getLogger(__name__)


class OSCServer(AbstractOSCServer):
    def __init__(self, host=None, port=None):
        super().__init__(host, port)
        self._dispatcher = Dispatcher()
        self._server: ThreadingOSCUDPServer = None
        self._message_handler = MessageHandler()

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

        self._message_handler.handle(address, values)
