from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.osc.mood import Mood


class FixtureGroup(BaseFixture):
    @dataclass
    class Mapping:
        """Dummy Mapping to conform to BaseFixture"""
        pass

    def __init__(self, fixtures, address: int = None):
        super().__init__(address)

        self.fixtures: list[BaseFixture] = fixtures
        # fixme: use a setter on fixtures to check too ?
        if any([isinstance(f, FixtureGroup) for f in self.fixtures]):
            raise ValueError("Nested fixture groups not supported")

    def map_to_channels(self, mood: Mood, group_position: float):
        channels = list()
        for group_index, fixture in enumerate(self.fixtures):
            channels += fixture.map_to_channels(mood, group_position=float(group_index) / (len(self.fixtures) - 1))
        return channels
