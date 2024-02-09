from abc import ABC, abstractmethod

from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.fixture.info import FixtureInfo


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
    def fixtures_info(self) -> list[FixtureInfo]:
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
