# fixme: seems not to be needed ?
from abc import ABC, abstractmethod

from oscartnetdaemon.entities.osc.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget


class AbstractOSCRecallGroupsRepository(ABC):

    @abstractmethod
    def create_groups(self, widgets: list[OSCAbstractWidget], recall_group_infos: list[OSCRecallGroupInfo]):
        pass

    @abstractmethod
    def save_for_slot(self, slot_name: str):
        pass

    @abstractmethod
    def recall_for_slot(self, slot_name: str):
        pass

    @abstractmethod
    def set_punch_for_slot(self, slot_name: str, is_punch: bool):
        pass