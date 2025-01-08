from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood


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

        self.dimmer = 1.0

    def update_mapping(self, mood: Mood, group_position: float):
        raise RuntimeError("Groups should not call this function")
