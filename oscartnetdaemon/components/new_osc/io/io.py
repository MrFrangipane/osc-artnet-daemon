from threading import Thread

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnetdaemon.components.new_osc.client_info import OSCClientInfo
from oscartnetdaemon.components.new_osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.new_osc.discovery.service import OSCDiscoveryService
from oscartnetdaemon.components.new_osc.io.message import OSCMessage
from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents


class OSCIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting

        self.discovery = OSCDiscoveryService(self, server_name="Frangitron's Oscarnet", server_port=8081)

        self.server: ThreadingOSCUDPServer | None = None
        self.server_thread: Thread | None = None

        self.clients_repository = OSCClientsRepository()

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

        self.discovery.start()

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        pass

    #
    # IO
    def handle_osc(self, client_address, osc_address, osc_value):
        self.components.io_message_queue_in.put(OSCMessage(osc_address=osc_address, osc_value=osc_value))

    def send_message(self, message: OSCMessage):
        clients = list(self.clients_repository.clients.values())  # avoid mutation during iteration (could be fixed ?)
        for client in clients:
            client.send_message(message.osc_address, message.osc_value)

    #
    # CLIENTS
    def register_client(self, client_info: OSCClientInfo):
        new_client = self.clients_repository.register(client_info)
        self.components.variable_repository.notify_all_variables()
        # self.recall_groups_repository.register_client(client_info)

    def unregister_client(self, client_info: OSCClientInfo):
        self.clients_repository.unregister(client_info)
        # self.recall_groups_repository.unregister_client(client_info)
