from abc import ABC, abstractmethod

from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl


class AbstractOSCControlRepository(ABC):

    @abstractmethod
    def create_controls(self, controls_infos: list) -> list[OSCAbstractControl]:
        pass

    @abstractmethod
    def map_to_dispatcher(self, dispatcher: object):
        pass

    @abstractmethod
    def get_all_controls_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        pass
