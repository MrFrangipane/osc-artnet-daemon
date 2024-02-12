import math
from abc import abstractmethod
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.abstract_metaclass import AbstractFixtureMetaclass
from oscartnetdaemon.core.mood import Mood


class BaseFixture(metaclass=AbstractFixtureMetaclass):

    @dataclass
    class Mapping:
        pass

    def __init__(self, address: int = None):
        self.address = address
        self.mood = Mood()
        self.group_position: float = 0.0

    @abstractmethod
    def map_to_channels(self) -> list[int]:
        pass

    def read_pattern(self, table, time_scale) -> float:
        beat_counter = self.mood.beat_counter * time_scale
        f_group_index = (len(table) - 1) * self.group_position
        # how expensive is that ?
        group_index = math.ceil(f_group_index) if f_group_index % 1 >= 0.5 else int(f_group_index)
        pattern_index = int(beat_counter % len(table[group_index]))

        return table[group_index][pattern_index]
