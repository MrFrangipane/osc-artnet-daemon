from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from artnet.io.message import ArtnetMessage


class ArtnetIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting, maybe a singleton ?

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        """
        pass

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        pass

    def send_message(self, message: ArtnetMessage):
        pass
