import logging
import time
from copy import copy
from dataclasses import fields

from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.core.components import Components

from oscartnetdaemon.components.fixtures.tristan_200 import Tristan200
from oscartnetdaemon.components.fixtures.octostrip_bar import OctostripBar
from oscartnetdaemon.components.fixtures.two_bright_par import TwoBrightPar
from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.fixture.group import FixtureGroup
from oscartnetdaemon.core.fixture.info import FixtureInfo

_logger = logging.getLogger(__name__)


class FixturesUpdater(AbstractFixturesUpdater):
    sleep_interval = 1.0 / 30

    def __init__(self):
        super().__init__()
        self._is_running = False

    # fixme: move this to a "session manager" class
    def load_fixtures(self):
        self._fixtures = [
            FixtureGroup([OctostripBar() for _ in range(8)]),
            Tristan200(),
            Tristan200(),
            FixtureGroup([TwoBrightPar() for _ in range(5)]),
        ]

    # fixme: move this to a "session manager" class
    def channels_info(self) -> list[ChannelInfo]:
        infos = list()
        dmx_index = 0
        group_index = 1
        fixture_index = 0
        for fixture in self._fixtures:
            if isinstance(fixture, FixtureGroup):
                for sub_fixture in fixture.fixtures:
                    for _ in fields(sub_fixture.Mapping):
                        infos.append(ChannelInfo(
                            dmx_index=dmx_index,
                            fixture_index=fixture_index,
                            group_index=group_index,
                            value=self.universe[dmx_index]
                        ))
                        dmx_index += 1
                    fixture_index += 1
                group_index += 1
            else:
                for _ in fields(fixture.Mapping):
                    infos.append(ChannelInfo(
                        dmx_index=dmx_index,
                        fixture_index=fixture_index,
                        group_index=0,
                        value=self.universe[dmx_index]
                    ))
                    dmx_index += 1
                fixture_index += 1
                group_index += 1

        return infos

    # fixme: move this to a "session manager" class
    def fixtures_info(self) -> list[FixtureInfo]:
        infos = list()
        dmx_index = 0
        group_index = 1
        fixture_index = 0
        for fixture in self._fixtures:
            if isinstance(fixture, FixtureGroup):
                for sub_fixture in fixture.fixtures:
                    infos.append(FixtureInfo(
                        name=f"{fixture_index:02d} {type(sub_fixture).__name__}",
                        channel_start=dmx_index,
                        channel_count=len(fields(sub_fixture.Mapping)),
                        group_index=group_index
                    ))
                    dmx_index += len(fields(sub_fixture.Mapping))
                    fixture_index += 1
                group_index += 1
            else:
                infos.append(FixtureInfo(
                    name=f"{fixture_index:02d} {type(fixture).__name__}",
                    channel_start=dmx_index,
                    channel_count=len(fields(fixture.Mapping)),
                    group_index=group_index
                ))
                dmx_index += len(fields(fixture.Mapping))
                fixture_index += 1
                group_index += 1

        return infos

    def start(self):
        _logger.info(f"Starting Fixture Updater")
        self._is_running = True

        while self._is_running:
            mood = copy(Components().mood)
            address_pointer = 0  # fixme: find better name

            for fixture in self._fixtures:
                channels = fixture.map_to_channels(mood, 0)
                start = address_pointer if fixture.address is None else fixture.address
                end = start + len(channels)

                _logger.debug(f"{type(fixture).__name__}({start}:{end}) = {channels}")
                self.universe[start:end] = channels
                address_pointer = end

            for artnet_server in Components().artnet_servers:
                artnet_server.set_universe(self.universe)

            time.sleep(self.sleep_interval)

    def stop(self):
        self._is_running = False

        self.universe = bytearray(512)
        for artnet_server in Components().artnet_servers:
            artnet_server.set_universe(self.universe)

        _logger.info(f"Fixture updater stopped, blackout")
