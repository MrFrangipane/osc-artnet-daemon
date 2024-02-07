import logging

from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.core.osc_client_info import OSCClientInfo

_logger = logging.getLogger(__name__)


class OSCClients:
    def __init__(self):
        self._clients: dict[bytes, SimpleUDPClient] = dict()
        self._clients_info: dict[bytes, OSCClientInfo] = dict()

    def create_client(self, info: OSCClientInfo):
        address = ".".join([str(int(b)) for b in info.address])
        self._clients[info.id] = SimpleUDPClient(address, info.port)
        self._clients_info[info.id] = info
        _logger.info(f"Add client {info}")

    def delete_client(self, client_id: bytes):
        _logger.info(f"Remove client {self._clients_info[client_id]}")
        self._clients.pop(client_id)
        self._clients_info.pop(client_id)

    def send(self, address, values):
        for client in self._clients.values():
            client.send_message(address, values)
