import logging
from ipaddress import IPv4Address

from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.core.osc_client_info import OSCClientInfo
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.components.osc.abstract_message_sender import AbstractOSCMessageSender
from oscartnetdaemon.components.pattern_store.api import PatternStoreAPI

_logger = logging.getLogger(__name__)


class OSCMessageSender(AbstractOSCMessageSender):
    def __init__(self):
        # TODO : dont register clients in two places (MoodStore + MessageSender)
        self._clients: dict[str, SimpleUDPClient] = dict()
        self._clients_info: dict[str, OSCClientInfo] = dict()

    def ensure_registered(self, ip_address: str, port: int):
        if ip_address not in self._clients:
            address_bytes = IPv4Address(ip_address).packed
            info = OSCClientInfo(
                address=address_bytes,
                id=address_bytes,
                name="Not discovered",
                port=port
            )
            self.register_client(info)
            Components().mood_store.register_client(info)  # FIXME

    def register_client(self, info: OSCClientInfo):
        ip_address = str(IPv4Address(info.address))
        _logger.info(f"Registering client {info.name} ({ip_address})")
        new_client = SimpleUDPClient(ip_address, info.port)

        self._clients[ip_address] = new_client
        self._clients_info[ip_address] = info

        _logger.debug(f"Sending /device_name, /device_address to {info.name}")
        new_client.send_message('/device_name', info.name)
        new_client.send_message('/device_address', ip_address)

        for pattern_index, pattern_name in enumerate(PatternStoreAPI.pattern_names()):
            new_client.send_message(f"/mood/pattern_name_{pattern_index}", pattern_name)

        self.send_mood_to_all()

    def unregister_client(self, info: OSCClientInfo):
        ip_address = str(IPv4Address(info.address))
        _logger.info(f"Unregistering client {info.name} ({ip_address})")
        self._clients.pop(ip_address)
        self._clients_info.pop(ip_address)

    def send(self, control_name, value, sender_ip):
        for ip_address, client in self._clients.items():

            # FIXME: very hacky
            bpm = Components().midi_tempo.info().bpm
            client.send_message(f"/mood/bpm_value", f"{bpm:.1f}")
            # FIXME: ----------

            if ip_address != sender_ip:
                address = f"/mood/{control_name}"
                _logger.debug(f"Sending message {address} {value}")
                client.send_message(address, value)

    def notify_punch(self, sender_ip, is_punch):
        _logger.debug(f"Notify punch from {sender_ip} {bool(is_punch)}")
        # todo: light a square on people's tablets ?

    def send_mood_to_all(self):
        for name, value in vars(Components().osc_state_model.mood).items():
            # fixme: use reflexion ? pack messages ?
            if name == "master_dimmer":
                continue
            self.send(name, value, "Server")

    def send_pattern_names_to_all(self):
        for pattern_index, pattern_name in enumerate(PatternStoreAPI.pattern_names()):
            self.send(f"pattern_name_{pattern_index}", pattern_name, "Server")

    def send_to_all_raw(self, address, value):
        for client in self._clients.values():
            client.send_message(address, value)
