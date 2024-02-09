from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood


class FixtureGroup:

    def __init__(self, fixtures, address: int = None):
        self.address = address
        self.fixtures: list[BaseFixture] = fixtures

    def map_to_channels(self, mood: Mood, group_position: float):
        channels = list()

        for group_index, fixture in enumerate(self.fixtures):
            channels += fixture.map_to_channels(mood, group_position=group_index / len(self.fixtures))

        return channels
