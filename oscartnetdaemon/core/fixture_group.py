from oscartnetdaemon.core.base_fixture import BaseFixture
from oscartnetdaemon.core.mood import Mood


class FixtureGroup(BaseFixture):
    def __init__(self, address, fixtures):
        super().__init__()
        self.address = address
        self.fixtures: list[BaseFixture] = fixtures

    @property
    def channels(self):
        return b"".join([fixture.channels for fixture in self.fixtures])

    def update(self, mood: Mood, group_position: float = 0):
        for group_index, fixture in enumerate(self.fixtures):
            fixture.update(mood, group_position=group_index / len(self.fixtures))
