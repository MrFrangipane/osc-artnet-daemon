from abc import ABC, abstractmethod

from oscartnetdaemon.entities.osc.widget_info import OSCWidgetInfo


class OSCAbstractWidget(ABC):

    def __init__(self, info: OSCWidgetInfo):
        self.info = info

    @abstractmethod
    def handle(self, client_address, osc_address, osc_value):
        pass

    @abstractmethod
    def get_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        pass
