from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from template.io.message import TemplateMessage


class TemplateIO(AbstractIO):

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

    def send_io_message(self, message: TemplateMessage):
        pass
