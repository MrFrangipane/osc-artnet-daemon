import logging

from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.core.osc_client_info import OSCClientInfo
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.components.osc.abstract_message_sender import AbstractOSCMessageSender

_logger = logging.getLogger(__name__)


class OSCMessageSender(AbstractOSCMessageSender):
    def __init__(self):
        self._clients: dict[str, SimpleUDPClient] = dict()
        self._clients_info: dict[str, OSCClientInfo] = dict()

    def register_client(self, info: OSCClientInfo):
        _logger.info(f"Registering client {info.name}")
        address = ".".join([str(int(b)) for b in info.address])
        new_client = SimpleUDPClient(address, info.port)

        self._clients[info.name] = new_client
        self._clients_info[info.name] = info

        _logger.debug(f"Sending '/device_name {info.name}' to {info.name}")
        new_client.send_message('/device_name', info.name)

        self.send_mood_to_all()

    def unregister_client(self, info: OSCClientInfo):
        _logger.info(f"Unregistering client {info.name}")
        self._clients.pop(info.name)
        self._clients_info.pop(info.name)

    def send(self, control_name, value, sender):
        for client_id in self._clients:
            client_name = self._clients_info[client_id].name

            # FIXME: very hacky
            bpm = Components().midi_tempo.bpm
            self._clients[client_name].send_message(f"/{client_name}/bpm_value", f"{bpm:.1f}")
            # FIXME: ----------

            if client_name != sender:
                address = f"/{client_name}/{control_name}"
                _logger.debug(f"Sending message {address} {value}")
                self._clients[client_id].send_message(address, value)

    def notify_punch(self, sender, is_punch):
        _logger.debug(f"Notify punch from {sender} {bool(is_punch)}")
        # todo: light a square on people's tablets ?

    def send_mood_to_all(self):
        for name, value in vars(Components().osc_state_model.mood).items():
            # fixme: use reflexion ? pack messages ?
            if name == "master_dimmer":
                continue
            self.send(name, value, "Server")

    def send_to_all_raw(self, address, value):
        for client_name in self._clients:
            self._clients[client_name].send_message(address, value)
