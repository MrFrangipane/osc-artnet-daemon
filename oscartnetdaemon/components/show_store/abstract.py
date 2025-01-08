from abc import ABC, abstractmethod

from oscartnetdaemon.core.show.show import Show
from oscartnetdaemon.core.show.item_info import ShowItemInfo
# from oscartnetdaemon.core.show.item import ShowItem
# FIXME circular dependency with BaseFixture


class AbstractShowStore(ABC):
    def __init__(self):
        self.show: Show = None
        self._fixtures_structure: list[list[str]] = list()

    @abstractmethod
    def load_show(self, fixtures_structure: list[list[str]]) -> None:
        pass

    @abstractmethod
    def reload_fixtures(self) -> None:
        pass

    @abstractmethod
    def items_by_type(self, type_name):
        pass

    @abstractmethod
    def item_by_info(self, show_item_info: ShowItemInfo):  # ShowItem
        pass
