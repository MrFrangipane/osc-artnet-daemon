from abc import ABC, abstractmethod

from oscartnetdaemon.core.show.show import Show


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
