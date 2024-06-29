from oscartnetdaemon.components.osc.discovery.clients import OSCDiscoveryClients
from oscartnetdaemon.components.osc.discovery.server import OSCDiscoveryServer


class OSCDiscoveryService:

    def __init__(self, io, server_name: str, server_port: int):
        self.clients = OSCDiscoveryClients(io)
        self.server = OSCDiscoveryServer(name=server_name, port=server_port)

    def start(self):
        self.clients.start()
        self.server.start()

    def stop(self):
        self.clients.stop()
        self.server.stop()
