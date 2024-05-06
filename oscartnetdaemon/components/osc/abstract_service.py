from abc import ABC, abstractmethod

from oscartnetdaemon.components.osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.osc.abstract_widget_repository import AbstractOSCWidgetRepository


class AbstractOSCService(ABC):

    @abstractmethod
    def __init__(self):
        self.clients_repository: OSCClientsRepository = None
        self.widget_repository: AbstractOSCWidgetRepository = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def send_to_all_clients(self, osc_address: str, osc_value: str | bytes | bool | int | float | list):
        pass
