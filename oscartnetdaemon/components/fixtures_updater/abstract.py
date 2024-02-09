from abc import ABC, abstractmethod

from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.fixture.base import BaseFixture


class AbstractFixturesUpdater(ABC):
    def __init__(self):
        self.universe = bytearray(512)

        self._fixtures: list[BaseFixture] = list()

    @abstractmethod
    def load_fixtures(self):
        pass

    @abstractmethod
    def channels_info(self) -> list[ChannelInfo]:
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
