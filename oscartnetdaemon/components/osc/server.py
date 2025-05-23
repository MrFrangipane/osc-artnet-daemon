import logging

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnetdaemon.components.osc.server_abstract import AbstractOSCServer
from oscartnetdaemon.components.osc.message_handler import MessageHandler

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
        self._server.dispatcher.set_default_handler(self._message_handler.handle, needs_reply_address=True)
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
        self._server.server_close()
        _logger.info(f"Last OSC message received {self._last_message_datetime}")
        _logger.info(f"OSC server stopped")
