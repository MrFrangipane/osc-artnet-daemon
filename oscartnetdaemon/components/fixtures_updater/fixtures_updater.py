import logging
import time
from copy import copy

from oscartnetdaemon.components.fixtures.one_pixel import OnePixel
from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.fixture_group import FixtureGroup

_logger = logging.getLogger(__name__)


class FixturesUpdater(AbstractFixturesUpdater):
    sleep_interval = 1.0 / 50

    def __init__(self):
        super().__init__()

        self._is_running = False
        self._artnet = Components().artnet

    def load_fixtures(self):
        self._fixtures.append(FixtureGroup(
            address=1,
            fixtures=[OnePixel() for _ in range(8)],
        ))

    def start(self):
        _logger.info(f"Starting fixture updater...")
        self._is_running = True
        while self._is_running:
            mood = copy(Components().mood)
            for fixture in self._fixtures:
                fixture.update(mood)
                channels = fixture.channels
                start = fixture.address
                end = fixture.address + len(channels)
                self.universe[start:end] = channels

            self._artnet.set_universe(self.universe)

            time.sleep(self.sleep_interval)

    def stop(self):
        self._is_running = False
        _logger.info(f"Fixture updater stopped")
