from threading import Thread

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.osc.configuration_loader import load_osc_configuration
from oscartnetdaemon.components.osc.controls.abstract_repository import AbstractOSCControlRepository
from oscartnetdaemon.components.osc.controls.repository import OSCControlRepository
from oscartnetdaemon.components.osc.entities.client_info import OSCClientInfo
from oscartnetdaemon.components.osc.recall.abstract_recall_groups_repository import AbstractOSCRecallGroupsRepository
from oscartnetdaemon.components.osc.recall.recall_groups_repository import OSCRecallGroupsRepository


class OSCService(AbstractImplementation):

    def __init__(self, configuration_info: ConfigurationInfo):
        super().__init__(configuration_info)
        self.osc_configuration = load_osc_configuration(self.configuration_info)

        self.clients_repository: OSCClientsRepository = None
        self.control_repository: AbstractOSCControlRepository = None
        self.recall_groups_repository: AbstractOSCRecallGroupsRepository = None

        self.server: ThreadingOSCUDPServer = None
        self._server_thread: Thread = None

    def initialize(self):
        # !! Called before process creation, don't create non-pickleable members here !!
        self.control_repository = OSCControlRepository()
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
