from threading import Thread

from pythonosc.osc_server import ThreadingOSCUDPServer, Dispatcher
from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.midi_osc_test_bridge.domain.abstract_implementation import AbstractImplementation
from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification
from oscartnetdaemon.midi_osc_test_bridge.osc.notification_origin import OSCNotificationOrigin


class OSCService(AbstractImplementation):
    ADDRESS = '/fader_pars/fader'

    def __init__(self, domain):
        super().__init__(domain)
        self.clients: dict[tuple[int], SimpleUDPClient] = dict()

    def start(self):
        dispatcher = Dispatcher()
        dispatcher.map(self.ADDRESS, self._handle, needs_reply_address=True)

        server = ThreadingOSCUDPServer(
            server_address=("192.168.20.7", 8080),
            dispatcher=dispatcher
        )

        server_thread = Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

    def _handle(self, remote, address, value):
        if remote[0] not in self.clients:
            self.clients[remote[0]] = SimpleUDPClient(address=remote[0], port=remote[1])

        self.domain.notify_change(ChangeNotification(
            origin=OSCNotificationOrigin(remote_ip=remote[0]),
            control_name='FaderA',
            value=value
        ))

    def handle_change_notification(self, change_notification: ChangeNotification):
        for client_ip, client in self.clients.items():
            if client_ip == change_notification.origin.remote_ip:
                continue

            client.send_message(self.ADDRESS, value=change_notification.value)
