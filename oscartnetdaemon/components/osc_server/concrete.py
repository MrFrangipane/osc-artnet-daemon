import logging
from datetime import datetime

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnetdaemon.components.osc_server.abstract import AbstractOSCServer
from oscartnetdaemon.components.osc_server.message_handler import MessageHandler
from oscartnetdaemon.core.components import Components

_logger = logging.getLogger(__name__)


class OSCServer(AbstractOSCServer):
    def __init__(self, address, port):
        super().__init__(address, port)

        self._dispatcher = Dispatcher()
        self._server: ThreadingOSCUDPServer = None
        self._message_handler = MessageHandler()

    def start(self):
        _logger.info(f"Starting OSC server (host={self.address}, port={self.port})")

        self._server = ThreadingOSCUDPServer(
            server_address=(self.address, self.port),
            dispatcher=self._dispatcher
        )
        self._server.dispatcher.set_default_handler(self._handle)
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
        _logger.info(f"Last OSC message received {self._last_message_datetime}")
        _logger.info(f"OSC server stopped")

    def _handle(self, address, *values):
        _logger.debug(f"{address} {values}")
        self._last_message_datetime = datetime.now()

        response_address, response_values = self._message_handler.handle(address, values)
        if response_address is not None:
            Components().osc_clients.send(response_address, response_values)
