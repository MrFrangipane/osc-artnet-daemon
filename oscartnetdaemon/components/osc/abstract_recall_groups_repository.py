# fixme: seems not to be needed ?
from abc import ABC, abstractmethod

from oscartnetdaemon.components.osc.entities.client_info import OSCClientInfo
from oscartnetdaemon.components.osc.entities.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl


class AbstractOSCRecallGroupsRepository(ABC):

    @abstractmethod
    def create_groups(self, controls: list[OSCAbstractControl], recall_group_infos: list[OSCRecallGroupInfo]):
        pass

    @abstractmethod
    def register_client(self, client_info: OSCClientInfo):
        pass

    @abstractmethod
    def unregister_client(self, client_info: OSCClientInfo):
        pass

    @abstractmethod
    def save_for_slot(self, slot_name: str):
        pass

    @abstractmethod
    def recall_for_slot(self, slot_name: str):
        pass

    @abstractmethod
    def set_punch_for_slot(self, client_info: OSCClientInfo, slot_name: str, is_punch: bool):
        pass
