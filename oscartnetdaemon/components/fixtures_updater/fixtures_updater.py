import logging
import time
from copy import copy

from oscartnetdaemon.components.fixtures_updater.abstract import AbstractFixturesUpdater
from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.osc.state_model import OSCStateModel
from oscartnetdaemon.core.show.item import ShowItem


from oscartnetfixtures.python_extensions.math import map_to_int  # FIXME !!

_logger = logging.getLogger(__name__)


class FixturesUpdater(AbstractFixturesUpdater):
    sleep_interval = 1.0 / 40

    def __init__(self):
        super().__init__()
        self._is_running = False
        self._pattern_edition_wheel_previous: float = 0.0

    def start(self):
        _logger.info(f"Starting Fixture Updater")
        self._is_running = True

        while self._is_running:
            if Components().osc_state_model.current_page == OSCStateModel.Page.Groups:
                self._groups()
            if Components().osc_state_model.current_page == OSCStateModel.Page.Tristan200:
                self._tristan_200()
            elif Components().osc_state_model.current_page == OSCStateModel.Page.TwoBrightPar:
                self._two_bright_par()
            elif Components().osc_state_model.current_page == OSCStateModel.Page.PatternEdition:
                self._pattern_edition()
            else:  # OSCStateModel.Page.Mood:
                self._mood()

            time.sleep(self.sleep_interval)

    def _groups(self):
        # fixme: Groups's variables are int, map to int should be done in message handler
        channels = [map_to_int(v) for v in vars(Components().osc_state_model.groups).values()]
        for i, mapping in enumerate(vars(Components().osc_state_model.groups).keys()):
            Components().osc_message_sender.send_to_all_raw(
                f"/#groups/{mapping}_value", f"{channels[i]:03d}"
            )
            Components().osc_message_sender.send_to_all_raw(
                f"/#groups/{mapping}", float(channels[i]) / 255.0
            )
            Components().show_store.show.groups_dimmers[i] = float(channels[i]) / 255.0

    def _tristan_200(self):
        # fixme: Tristan200's variables are int, map to int should be done in message handler
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

    def _two_bright_par(self):
        # FIXME this does not exist anymore in the TOSC file
        show_items = Components().show_store.items_by_type(Components().osc_state_model.current_page.name)
        colors = Components().osc_state_model.two_bright_par.pars

        for par_index, show_item in enumerate(show_items):
            if par_index >= len(colors):
                continue
            color = colors[par_index]
            channels = show_item.fixture.map_from_hsl(color)  # fixme: no one knows this function exists !
            self.universe[show_item.channel_first:show_item.channel_last] = channels

    def _pattern_edition(self):
        wheel = Components().osc_state_model.pattern_edition.wheel
        if wheel != self._pattern_edition_wheel_previous:
            self._pattern_edition_wheel_previous = wheel
            Components().pattern_store.wheel_changed(wheel)

    def _mood(self):
        # fixme: create a component that transforms OSC model to FixtureUpdater model
        # todo: add a "last midi message" timestamp to let fixtures deal with time if no midi was received ?
        mood = copy(Components().osc_state_model.mood)
        mood.bpm = Components().midi_tempo.bpm
        mood.beat_counter = Components().midi_tempo.beat_counter

        for show_item in Components().show_store.show.items:
            # fixme: better models please (ShowItem, Fixture, ...)
            show_item.fixture.group_position = show_item.group.position
            show_item.fixture.group_place = show_item.group.place
            show_item.fixture.group_size = show_item.group.size
            show_item.fixture.mood = mood
            group_dimmer = Components().show_store.show.groups_dimmers[
                show_item.group.index - 1]  # FIXME this should be starting at 0
            channels = show_item.fixture.map_to_channels(group_dimmer)
            self.universe[show_item.channel.first:show_item.channel.last] = channels

        for artnet_server in Components().artnet_servers:
            artnet_server.set_universe(self.universe)

    def stop(self):
        self._is_running = False

        self.universe = bytearray(512)
        for artnet_server in Components().artnet_servers:
            artnet_server.set_universe(self.universe)

        _logger.info(f"Fixture updater stopped, blackout")

    def channels_info(self) -> list[ChannelInfo]:
        infos = list()
        for show_item in Components().show_store.show.items:
            for dmx_index in range(show_item.channel.first, show_item.channel.last):
                channel_info = ChannelInfo(
                    dmx_index=dmx_index,
                    fixture_index=show_item.fixture_index,
                    group_index=show_item.group.index,
                    value=self.universe[dmx_index]
                )
                infos.append(channel_info)
        return infos

    def set_pattern_edition_step(slef, show_item: ShowItem, step: dict[str, int]):
        print(f"show_pattern_step: {show_item} {step}")
