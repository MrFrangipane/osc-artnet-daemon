from multiprocessing import Queue
from threading import Thread

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.osc.configuration_loader import load_osc_configuration
from oscartnetdaemon.components.osc.controls.repository import OSCControlRepository
from oscartnetdaemon.components.osc.entities.client_info import OSCClientInfo
from oscartnetdaemon.components.osc.recall.abstract_recall_groups_repository import AbstractOSCRecallGroupsRepository
from oscartnetdaemon.components.osc.recall.recall_groups_repository import OSCRecallGroupsRepository


class OSCService(AbstractImplementation):

    def __init__(self, configuration_info: ConfigurationInfo):
        super().__init__(configuration_info)
        self.osc_configuration = load_osc_configuration(self.configuration_info)

        self.clients_repository: OSCClientsRepository = None
        self.control_repository: OSCControlRepository = None
        self.recall_groups_repository: AbstractOSCRecallGroupsRepository = None

        self.server: ThreadingOSCUDPServer = None
        self._server_thread: Thread = None

        self.osc_messages_queue = Queue()

    def initialize(self):
        # !! Called before process creation, don't create non-pickleable members here !!
        self.control_repository = OSCControlRepository(service=self)
        controls = self.control_repository.create_controls(self.osc_configuration.controls)

        self.recall_groups_repository = OSCRecallGroupsRepository()
        self.recall_groups_repository.create_groups(
            controls=controls,
            recall_group_infos=self.osc_configuration.recall_groups
        )

        self.clients_repository = OSCClientsRepository()

    def exec(self):
        dispatcher = Dispatcher()
        self.control_repository.map_to_dispatcher(dispatcher)

        address = self.osc_configuration.server_ip_address
        port = self.osc_configuration.server_port
        self.server = ThreadingOSCUDPServer(
            server_address=(address, port),
            dispatcher=dispatcher
        )

        self._server_thread: Thread = Thread(target=self.server.serve_forever, daemon=True)
        self._server_thread.start()

        while True:
            while not self.notification_queue_in.empty():
                change_notification = self.notification_queue_in.get()
                self.control_repository.forward_change_notification(change_notification)

            while not self.osc_messages_queue.empty():
                address, value = self.osc_messages_queue.get()
                self.send_message(address, value)

    def handle_termination(self):
        pass

    #
    # CLIENTS
    def register_client(self, client_info: OSCClientInfo):
        new_client = self.clients_repository.register(client_info)
        for osc_address, osc_value in self.control_repository.get_all_controls_update_messages():
            new_client.send_message(osc_address, osc_value)
        self.recall_groups_repository.register_client(client_info)

    def unregister_client(self, client_info: OSCClientInfo):
        self.clients_repository.unregister(client_info)
        self.recall_groups_repository.unregister_client(client_info)

    def send_message(self, osc_address: str, osc_value: str | bytes | bool | int | float | list):
        clients = list(self.clients_repository.clients.values())  # avoid mutation during iteration (could be fixed ?)
        for client in clients:
            client.send_message(osc_address, osc_value)
