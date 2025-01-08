from abc import abstractmethod
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.abstract_metaclass import AbstractFixtureMetaclass
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo
from oscartnetdaemon.components.pattern_store.api import PatternStoreAPI


class BaseFixture(metaclass=AbstractFixtureMetaclass):

    @dataclass
    class Mapping:
        pass

    def __init__(self, address: int = None):
        self.address = address
        self._mapping = self.Mapping()

    @abstractmethod
    def map_to_channels(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo) -> list[int]:
        pass
