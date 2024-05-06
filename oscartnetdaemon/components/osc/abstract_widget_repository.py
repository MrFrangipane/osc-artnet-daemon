from abc import ABC, abstractmethod


class AbstractOSCWidgetRepository(ABC):

    @abstractmethod
    def create_widgets(self, widget_infos: list):
        pass

    @abstractmethod
    def map_to_dispatcher(self, dispatcher: object):
        pass

    @abstractmethod
    def get_all_widget_update_messages(self) -> list[tuple[str, int | bool | float | str | list]]:
        pass
