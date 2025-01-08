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

    def apply_pattern_step(self, step: dict[str, int]):
        self._mapping = self.Mapping()
        for parameter, value in step.items():
            setattr(self._mapping, parameter, value)

    def apply_pattern_while_playing(self, group_info: ShowItemGroupInfo):
        step = PatternStoreAPI.get_step_while_playing(
            fixture_type=self.__class__.__name__,
            group_place=group_info.place
        )
        self.apply_pattern_step(step=step)

    def map_to_channels(self):
        return list(vars(self._mapping).values())

    @abstractmethod
    def update_mapping(self, mood: Mood, dimmer_value: float, group_info: ShowItemGroupInfo) -> list[int]:
        pass
