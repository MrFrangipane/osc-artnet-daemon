from threading import Thread

from pythonosc.osc_server import ThreadingOSCUDPServer, Dispatcher
from pythonosc.udp_client import SimpleUDPClient

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.domain.control.float import FloatValue
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.osc.notification_origin import OSCNotificationOrigin


class OSCService(AbstractImplementation):
    ADDRESS = '/fader_pars/fader'

    def __init__(self, configuration_info: ConfigurationInfo):
        super().__init__(configuration_info)
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

        self.notifications_queue_out.put(ChangeNotification(
            origin=OSCNotificationOrigin(remote_ip=remote[0]),
            control_name='octostrip',
            value=FloatValue(value)
        ))

    def loop(self):
        while True:
            change_notification = self.notification_queue_in.get()
            for client_ip, client in self.clients.items():
                if isinstance(change_notification.origin, OSCNotificationOrigin) and client_ip == change_notification.origin.remote_ip:
                    continue

                client.send_message(self.ADDRESS, value=change_notification.value.value)

    def handle_termination(self):
        pass
