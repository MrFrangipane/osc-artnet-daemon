from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from simpledmxconsole.artnet.io.artnet_server import ArtnetServer
from simpledmxconsole.artnet.io.message import ArtnetIOMessage


class ArtnetIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting, maybe a singleton ?
        self.server = ArtnetServer()
        self.universe = bytearray(512)

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        """
        self.server.start()

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        self.server.stop()

    def send_io_message(self, message: ArtnetIOMessage):
        self.universe[message.channel] = message.value
        self.server.set_universe(self.universe)
