from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from yourproject.template.io.message import TemplateMessage


class TemplateIO(AbstractIO):

    def __init__(self, components: ServiceComponents):
        super().__init__(components)
        self.components: ServiceComponents = components  # FIXME: circular import forbids type hinting, maybe a singleton ?

    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        If needed, initialize variables values
        (broadcast happens after all services are started, in service registration order)
        """
        pass

    def shutdown(self):
        """
        Gracefully shutdown all IO, Thread, Process, ... that start() may have opened
        """
        pass

    def send_io_message(self, message: TemplateMessage):
        pass