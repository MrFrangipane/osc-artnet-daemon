from threading import Thread

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.udp_client import UDPClient

from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents


class OSCIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.server: ThreadingOSCUDPServer | None = None
        self.server_thread: Thread | None = None

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        """
        dispatcher = Dispatcher()
        dispatcher.set_default_handler(self.handle_osc, needs_reply_address=True)

        address = self.components.configuration.server_ip_address
        port = self.components.configuration.server_port
        self.server = ThreadingOSCUDPServer(
            server_address=(address, port),
            dispatcher=dispatcher
        )
        self.server_thread: Thread = Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def handle_osc(self, client_address, osc_address, osc_value):
        # self.components.io_message_queue_in.put()
        print(client_address, osc_address, osc_value)

    def shutdown(self):
        """
        Gracefully shutdown all IO
        """
        pass
