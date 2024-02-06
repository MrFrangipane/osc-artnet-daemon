import time
from copy import copy

from oscartnetdaemon.components.fixtures.one_pixel import OnePixel
from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.fixture_group import FixtureGroup


class FixturesUpdater(AbstractFixturesUpdater):
    sleep_interval = 1.0 / 50

    def __init__(self):
        super().__init__()
        self._universe = bytearray(512)
        self._mood = Components().mood
        self._artnet = Components().artnet

    def load_fixtures(self):
        self._fixtures.append(FixtureGroup(
            address=1,
            fixtures=[OnePixel() for _ in range(8)],
        ))

    def start(self):
        while True:
            mood = copy(self._mood)
            for fixture in self._fixtures:
                fixture.update(mood)
                channels = fixture.channels
                start = fixture.address
                end = fixture.address + len(channels)
                self._universe[start:end] = channels

            self._artnet.set_universe(self._universe)

            time.sleep(self.sleep_interval)
