import logging
import time

from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.core.osc_client_info import OSCClientInfo

_logger = logging.getLogger(__name__)


class OSCMessageSender:
    def __init__(self):
        self._clients: dict[bytes, SimpleUDPClient] = dict()
        self._clients_info: dict[bytes, OSCClientInfo] = dict()

    def create_client(self, info: OSCClientInfo):
        _logger.info(f"Adding client {info}")
        address = ".".join([str(int(b)) for b in info.address])
        new_client = SimpleUDPClient(address, info.port)

        self._clients[info.id] = new_client
        self._clients_info[info.id] = info

        _logger.debug(f"Sending '/device_name {info.name}' to {info}")
        new_client.send_message('/device_name', info.name)

    def delete_client(self, client_id: bytes):
        _logger.info(f"Removing client {self._clients_info[client_id]}")
        self._clients.pop(client_id)
        self._clients_info.pop(client_id)

    def send(self, control_name, value, sender):
        for client_id in self._clients:
            name = self._clients_info[client_id].name
            if name != sender:
                address = f"/{name}/{control_name}"
                _logger.debug(f"Sending message {address} {value}")
                self._clients[client_id].send_message(address, value)
