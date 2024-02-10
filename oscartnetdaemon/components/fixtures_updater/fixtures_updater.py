import logging
import time
from copy import copy
from dataclasses import fields

from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.python_extensions.math import map_to_int

from oscartnetdaemon.components.fixtures.tristan_200 import Tristan200
from oscartnetdaemon.components.fixtures.octostrip_bar import OctostripBar
from oscartnetdaemon.components.fixtures.two_bright_par import TwoBrightPar
from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.fixture.group import FixtureGroup
from oscartnetdaemon.core.osc.state_model import OSCStateModel

_logger = logging.getLogger(__name__)


class FixturesUpdater(AbstractFixturesUpdater):
    sleep_interval = 1.0 / 30

    def __init__(self):
        super().__init__()
        self._is_running = False

    def start(self):
        _logger.info(f"Starting Fixture Updater")
        self._is_running = True

        while self._is_running:
            if Components().osc_state_model.current_page == OSCStateModel.Page.Mood:
                mood = copy(Components().osc_state_model.mood)

                for show_item in Components().show_store.show.items:
                    channels = show_item.fixture.map_to_channels(mood, 0)
                    self.universe[show_item.channel_first:show_item.channel_last] = channels

                for artnet_server in Components().artnet_servers:
                    artnet_server.set_universe(self.universe)

            elif Components().osc_state_model.current_page == OSCStateModel.Page.Tristan200:
                tristans = list()
                for fixture in self._fixtures:
                    if isinstance(fixture, FixtureGroup):
                        for sub_fixture in fixture.fixtures:
                            if isinstance(sub_fixture, Tristan200):
                                tristans.append(sub_fixture)
                    elif isinstance(fixture, Tristan200):
                        tristans.append(fixture)

                channels = [map_to_int(v) for v in vars(Components().osc_state_model.tristan_200).values()]
                for tristan in tristans:
                    # fixme: implies that address is set (and in artnet 1-based!) !
                    start = tristan.address
                    end = start + len(channels)
                    self.universe[start:end] = channels

            time.sleep(self.sleep_interval)

    def stop(self):
        self._is_running = False

        self.universe = bytearray(512)
        for artnet_server in Components().artnet_servers:
            artnet_server.set_universe(self.universe)

        _logger.info(f"Fixture updater stopped, blackout")

    def channels_info(self) -> list[ChannelInfo]:
        infos = list()
        for show_item in Components().show_store.show.items:
            for dmx_index in range(show_item.channel_first, show_item.channel_last):
                channel_info = ChannelInfo(
                    dmx_index=dmx_index,
                    fixture_index=show_item.fixture_index,
                    group_index=show_item.group_index,
                    value=self.universe[dmx_index]
                )
                infos.append(channel_info)
        return infos
