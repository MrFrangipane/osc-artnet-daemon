from threading import Thread

from pythonosc.osc_server import ThreadingOSCUDPServer, Dispatcher

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.osc.abstract_service import AbstractOSCService
from oscartnetdaemon.components.osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.osc.widget_repository import OSCWidgetRepository
from oscartnetdaemon.entities.osc.client_info import OSCClientInfo


class OSCService(AbstractOSCService):

    def __init__(self):
        super().__init__()
        self.server: ThreadingOSCUDPServer = None

        self._server_thread: Thread = None
        self._clients_pool_thread: Thread = None

    def _initialize(self):
        configuration = Components().osc_configuration

        self.widget_repository = OSCWidgetRepository()
        self.widget_repository.create_widgets(configuration.widgets)

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
