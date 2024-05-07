from abc import ABC, abstractmethod

from oscartnetdaemon.components.osc.clients_repository import OSCClientsRepository
from oscartnetdaemon.components.osc.abstract_recall_groups_repository import AbstractOSCRecallGroupsRepository

# fixme: test to see if abstract is necessary
from oscartnetdaemon.components.osc.recall_groups_repository import OSCRecallGroupsRepository

from oscartnetdaemon.components.osc.abstract_widget_repository import AbstractOSCWidgetRepository
from oscartnetdaemon.entities.osc.client_info import OSCClientInfo


class AbstractOSCService(ABC):

    @abstractmethod
    def __init__(self):
        self.clients_repository: OSCClientsRepository = None
        self.widget_repository: AbstractOSCWidgetRepository = None
        self.recall_groups_repository: AbstractOSCRecallGroupsRepository = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def send_to_all_clients(self, osc_address: str, osc_value: str | bytes | bool | int | float | list):
        pass

    @abstractmethod
    def register_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def unregister_client(self, info: OSCClientInfo):
        pass

    @abstractmethod
    def save_for_slot(self, osc_address: str):
        pass

    @abstractmethod
    def recall_for_slot(self, osc_address: str):
        pass

    @abstractmethod
    def set_punch_for_slot(self, osc_address: str, is_punch: bool):
        pass
