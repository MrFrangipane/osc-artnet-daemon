from abc import ABC, abstractmethod
from typing import Any

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo
from oscartnetdaemon.components.domain.value.abstract import AbstractValue


class OSCAbstractControl(ABC):

    def __init__(self, info: OSCControlInfo, service: "OSCService"):
        self.service = service
        self.info: OSCControlInfo = info
        self.value: AbstractValue | None = None

    @abstractmethod
    def handle_osc(self, client_address, osc_address, osc_value):
        pass

    @abstractmethod
    def handle_notification(self, change_notification: ChangeNotification):
        pass

    @abstractmethod
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        pass

    @abstractmethod
    def get_values(self) -> Any:
        pass

    @abstractmethod
    def set_values(self, values: Any):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__}(info.osc_address={self.info.osc_address})>"
