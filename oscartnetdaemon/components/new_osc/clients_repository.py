import logging

from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.components.new_osc.client_info import OSCClientInfo
from oscartnetdaemon.python_extensions.network import bytes_as_ip, ip_as_bytes


_logger = logging.getLogger(__name__)


class OSCClientsRepository:
    def __init__(self):
        self.clients: dict[str, SimpleUDPClient] = dict()
        self._client_infos: dict[str, OSCClientInfo] = dict()

    def register(self, info: OSCClientInfo) -> SimpleUDPClient:
        address = bytes_as_ip(info.address)
        _logger.info(f"Registering client {info.name} ({address})")
        new_client = SimpleUDPClient(address, info.port)

        self.clients[info.name] = new_client
        self._client_infos[info.name] = info

        return new_client

    def unregister(self, info: OSCClientInfo):
        address = bytes_as_ip(info.address)
        _logger.info(f"Unregistering client {info.name} ({address})")
        self.clients.pop(info.name)
        self._client_infos.pop(info.name)

    def get_client_info_by_ip(self, client_ip_address: str) -> OSCClientInfo:
        client_ip_address = ip_as_bytes(client_ip_address)
        for client_info in self._client_infos.values():
            if client_info.address == client_ip_address:
                return client_info
