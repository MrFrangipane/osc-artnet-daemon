import time
from copy import copy

from oscartnet.components.fixtures.one_pixel import OnePixel
from oscartnet.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnet.core.components import Components


class FixturesUpdater(AbstractFixturesUpdater):
    sleep_interval = 1.0 / 50

    def __init__(self):
        super().__init__()
        self._universe = bytearray(512)
        self._mood = Components().mood
        self._artnet = Components().artnet

    def load_fixtures(self):
        self._fixtures.append(OnePixel(address=1))

    def start(self):
        while True:

            for fixture in self._fixtures:
                fixture.update(copy(self._mood))
                start = fixture.address
                end = fixture.address + len(fixture.channels)
                self._universe[start:end] = fixture.channels

            self._artnet.set_universe(self._universe)

            time.sleep(self.sleep_interval)
