from abc import ABC, abstractmethod


class AbstractFixturesUpdater(ABC):
    def __init__(self):
        self.universe = bytearray(512)

        self._fixtures = list()

    @abstractmethod
    def load_fixtures(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
