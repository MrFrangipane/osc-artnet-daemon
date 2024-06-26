from abc import ABC, abstractmethod

# FIXME: circular import
# from oscartnetdaemon.domain_contract.service_components import ServiceComponents


class AbstractIO(ABC):

    def __init__(self, components: "ServiceComponents"):
        self.components = components

    @abstractmethod
    def start(self):
        """
        Start IO loop without blocking, deal with in and out queues
        """
        pass

    @abstractmethod
    def shutdown(self):
        """
        Gracefully shutdown all IO
        """
        pass
