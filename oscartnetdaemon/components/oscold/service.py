from threading import Thread

from pythonosc.osc_server import ThreadingOSCUDPServer, Dispatcher

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.abstract_service import AbstractOSCService
from oscartnetdaemon.components.osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.osc.control_repository import OSCControlRepository
from oscartnetdaemon.components.osc.entities.client_info import OSCClientInfo
from oscartnetdaemon.components.osc.recall_groups_repository import OSCRecallGroupsRepository


class OSCService(AbstractOSCService):

    def __init__(self):
        super().__init__()
        self.server: ThreadingOSCUDPServer = None
        self._server_thread: Thread = None

    def _initialize(self):
        configuration = Components().osc_configuration

        self.control_repository = OSCControlRepository()
        controls = self.control_repository.create_controls(configuration.controls)

        self.recall_groups_repository = OSCRecallGroupsRepository()
        self.recall_groups_repository.create_groups(
            controls=controls,
            recall_group_infos=configuration.recall_groups
        )

        self.clients_repository = OSCClientsRepository()

        dispatcher = Dispatcher()
        self.control_repository.map_to_dispatcher(dispatcher)

        address = configuration.server_ip_address
        port = configuration.server_port
        self.server = ThreadingOSCUDPServer(
            server_address=(address, port),
            dispatcher=dispatcher
        )

    def start(self):
        self._initialize()

        self._server_thread: Thread = Thread(target=self.server.serve_forever, daemon=True)
        self._server_thread.start()

    def stop(self):
        raise NotImplementedError()

    def send_message(self, osc_address: str, osc_value: str | bytes | bool | int | float | list):
        clients = list(self.clients_repository.clients.values())  # avoid mutation during iteration (could be fixed ?)
        for client in clients:
            client.send_message(osc_address, osc_value)

    def register_client(self, client_info: OSCClientInfo):
        new_client = self.clients_repository.register(client_info)
        for osc_address, osc_value in self.control_repository.get_all_controls_update_messages():
            new_client.send_message(osc_address, osc_value)
        self.recall_groups_repository.register_client(client_info)

    def unregister_client(self, client_info: OSCClientInfo):
        self.clients_repository.unregister(client_info)
        self.recall_groups_repository.unregister_client(client_info)

    def save_for_slot(self, osc_address: str):
        self.recall_groups_repository.save_for_slot(osc_address)

    def recall_for_slot(self, osc_address: str):
        self.recall_groups_repository.recall_for_slot(osc_address)

    def set_punch_for_slot(self, client_info: OSCClientInfo, osc_address: str, is_punch: bool):
        self.recall_groups_repository.set_punch_for_slot(client_info, osc_address, is_punch)

    def client_info_from_ip(self, client_ip_address: str) -> OSCClientInfo:
        return self.clients_repository.get_client_info_by_ip(client_ip_address)

    def notify_update(self, control_name, value):
        control = self.control_repository.control_from_mapping(control_name)
        if control is not None:
            pass
            # control.set_values()
