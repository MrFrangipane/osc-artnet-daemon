import logging
import time
from copy import copy

from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.osc.state_model import OSCStateModel

from oscartnetfixtures.python_extensions.math import map_to_int  # FIXME !!

_logger = logging.getLogger(__name__)


class FixturesUpdater(AbstractFixturesUpdater):
    sleep_interval = 1.0 / 40

    def __init__(self):
        super().__init__()
        self._is_running = False

    def start(self):
        _logger.info(f"Starting Fixture Updater")
        self._is_running = True

        while self._is_running:
            if Components().osc_state_model.current_page == OSCStateModel.Page.Mood:
                # fixme: create a component that transforms OSC model to FixtureUpdater model
                # todo: add a "last midi message" timestamp to let fixtures deal with time if no midi was received ?
                mood = copy(Components().osc_state_model.mood)
                mood.bpm = Components().midi_tempo.bpm
                mood.beat_counter = Components().midi_tempo.beat_counter

                for show_item in Components().show_store.show.items:
                    # fixme: better models please (ShowItem, Fixture, ...)
                    show_item.fixture.group_position = show_item.group_position
                    show_item.fixture.mood = mood
                    channels = show_item.fixture.map_to_channels()
                    self.universe[show_item.channel_first:show_item.channel_last] = channels

                for artnet_server in Components().artnet_servers:
                    artnet_server.set_universe(self.universe)

            # fixme later: dont rely on actual Fixtures (use reflection, Fixture.Mapping, etc)
            elif Components().osc_state_model.current_page == OSCStateModel.Page.Tristan200:
                channels = [map_to_int(v) for v in vars(Components().osc_state_model.tristan_200).values()]

                show_items = Components().show_store.items_by_type(Components().osc_state_model.current_page.name)
                for show_item in show_items:
                    self.universe[show_item.channel_first:show_item.channel_last] = channels

                for i, mapping in enumerate(vars(Components().osc_state_model.tristan_200).keys()):
                    # fixme: pack messages ?
                    Components().osc_message_sender.send_to_all_raw(
                        f"/#tristan_200/{mapping}_value", f"{channels[i]:03d}"
                    )
                    Components().osc_message_sender.send_to_all_raw(
                        f"/#tristan_200/{mapping}", float(channels[i]) / 255.0
                    )

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
