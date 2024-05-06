from oscartnetdaemon.components.discovery.server import DiscoveryServer
from oscartnetdaemon.components.discovery.clients import DiscoveryClients


class DiscoveryService:

    def __init__(self, server_name: str, server_port: int):
        self.clients = DiscoveryClients()
        self.server = DiscoveryServer(name=server_name, port=server_port)

    def start(self):
        self.clients.start()
        self.server.start()

    def stop(self):
        self.clients.stop()
        self.server.stop()
