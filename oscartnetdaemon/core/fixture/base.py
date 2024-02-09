from abc import abstractmethod
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.abstract_metaclass import AbstractFixtureMetaclass
from oscartnetdaemon.core.osc.mood import Mood


class BaseFixture(metaclass=AbstractFixtureMetaclass):

    @dataclass
    class Mapping:
        pass

    def __init__(self, address: int = None):
        self.address = address

    @abstractmethod
    def map_to_channels(self, mood: Mood, group_position: float) -> list[int]:
        pass
