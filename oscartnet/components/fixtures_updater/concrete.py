from copy import copy

from oscartnet.components.fixtures.one_pixel import OnePixel
from oscartnet.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnet.core.components import Components


class FixturesUpdater(AbstractFixturesUpdater):
    def __init__(self):
        super().__init__()
        self._is_running = False
        self._universe = bytearray(512)

    def load_fixtures(self):
        self._fixtures.append(OnePixel(address=1))

    def start(self):
        self._is_running = True
        while self._is_running:

            mood = copy(Components().mood)
            for fixture in self._fixtures:
                fixture.update(mood)
                start = fixture.address
                end = fixture.address + len(fixture.channels)
                self._universe[start:end] = fixture.channels

            Components().artnet.set_universe(self._universe)

    def stop(self):
        self._is_running = False
