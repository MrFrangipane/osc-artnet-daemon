from threading import Thread

from pythonosc.osc_server import ThreadingOSCUDPServer, Dispatcher
from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.midi_osc_test_bridge.implementation.abstract import AbstractImplementation
from oscartnetdaemon.midi_osc_test_bridge.domain.change_notification import ChangeNotification
from oscartnetdaemon.midi_osc_test_bridge.osc.notification_origin import OSCNotificationOrigin
from oscartnetdaemon.midi_osc_test_bridge.domain.controls import FloatControlValue


class OSCService(AbstractImplementation):
    ADDRESS = '/fader_pars/fader'

    def __init__(self):
        super().__init__()
        self.clients: dict[tuple[int], SimpleUDPClient] = dict()

    def exec(self):
        dispatcher = Dispatcher()
        dispatcher.map(self.ADDRESS, self._handle, needs_reply_address=True)

        server = ThreadingOSCUDPServer(
            server_address=("192.168.20.7", 8080),
            dispatcher=dispatcher
        )

        server_thread = Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        self.loop()

    def _handle(self, remote, address, value):
        if remote[0] not in self.clients:
            self.clients[remote[0]] = SimpleUDPClient(address=remote[0], port=remote[1])

        self.out_notifications.put(ChangeNotification(
            origin=OSCNotificationOrigin(remote_ip=remote[0]),
            control_name='FaderA',
            value=FloatControlValue(value)
        ))

    def loop(self):
        while True:
            change_notification = self.in_notifications.get()
            for client_ip, client in self.clients.items():
                if isinstance(change_notification.origin, OSCNotificationOrigin) and client_ip == change_notification.origin.remote_ip:
                    continue

                client.send_message(self.ADDRESS, value=change_notification.value.value)

    def handle_termination(self):
        pass
