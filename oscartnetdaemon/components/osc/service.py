from threading import Thread

from pythonosc.osc_server import ThreadingOSCUDPServer, Dispatcher

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.abstract_service import AbstractOSCService
from oscartnetdaemon.components.osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.osc.widget_repository import OSCWidgetRepository
from oscartnetdaemon.entities.osc.client_info import OSCClientInfo
from oscartnetdaemon.components.osc.recall_groups_repository import OSCRecallGroupsRepository


class OSCService(AbstractOSCService):

    def __init__(self):
        super().__init__()
        self.server: ThreadingOSCUDPServer = None

        self._server_thread: Thread = None
        self._clients_pool_thread: Thread = None

    def _initialize(self):
        configuration = Components().osc_configuration

        self.widget_repository = OSCWidgetRepository()
        widgets = self.widget_repository.create_widgets(configuration.widgets)

        self.recall_groups_repository = OSCRecallGroupsRepository()
        self.recall_groups_repository.create_groups(
            widgets=widgets,
            recall_group_infos=configuration.recall_groups
        )

        self.clients_repository = OSCClientsRepository()

        dispatcher = Dispatcher()
        self.widget_repository.map_to_dispatcher(dispatcher)

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

    def send_to_all_clients(self, osc_address: str, osc_value: str | bytes | bool | int | float | list):
        clients = list(self.clients_repository.clients.values())  # avoid mutation during iteration (could be fixed ?)
        for client in clients:
            client.send_message(osc_address, osc_value)

    def register_client(self, info: OSCClientInfo):
        new_client = self.clients_repository.register(info)
        for osc_address, osc_value in self.widget_repository.get_all_widget_update_messages():
            new_client.send_message(osc_address, osc_value)

    def unregister_client(self, info: OSCClientInfo):
        self.clients_repository.unregister(info)

    def save_for_slot(self, osc_address: str):
        # fixme: needs the recall group name !! (or uunique slot names, but not great)
        self.recall_groups_repository.save_for_slot(osc_address)

    def recall_for_slot(self, osc_address: str):
        self.recall_groups_repository.recall_for_slot(osc_address)

    def set_punch_for_slot(self, osc_address: str, is_punch: bool):
        self.recall_groups_repository.set_punch_for_slot(osc_address, is_punch)
