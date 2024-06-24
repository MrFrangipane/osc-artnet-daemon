from abc import ABC, abstractmethod
from typing import Any

from oscartnetdaemon.components.domain.entities.control_update_origin_enum import DomainControlUpdateOrigin
from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo


class OSCAbstractControl(ABC):

    def __init__(self, info: OSCControlInfo):
        self.info = info
        self.value = None
        self.components_singleton = None  # FIXME: WTF is that ?!

    def handle(self, client_address, osc_address, osc_value):
        self.on_change(client_address, osc_address, osc_value)
        self.notify_domain_control()

    def notify_domain_control(self):
        if self.info.mapped_to:
            self.components_singleton().domain_service.notify_update(
                origin=DomainControlUpdateOrigin.OSC,
                control_name=self.info.mapped_to,
                value=self.value
            )

    @abstractmethod
    def on_change(self, client_address, osc_address, osc_value):
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

    def send_osc(self, address, value):
        self.components_singleton().osc_service.make_message(
            osc_address=self.info.osc_address + address,
            osc_value=value
        )
