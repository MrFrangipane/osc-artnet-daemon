import logging
import time

from oscartnetdaemon.core.components import Components
from oscartnetdaemon.components.midi_tempo.abstract import AbstractMIDITempo
from oscartnetdaemon.core.midi_tempo_info import MIDITempoInfo


_logger = logging.getLogger(__name__)


class FallbackTapMidiTempo(AbstractMIDITempo):
    MaxBpm = 240

    def __init__(self):
        self._is_tapping = False
        self._first_tap = 0
        self._latest_tap = 0
        self._tap_count = 0

        self._beat_origin = 0

        self._bpm = 120
        self._beat_counter = 0

        self._is_running = False

        self._minimum_tap_interval = 60 / self.MaxBpm

    def is_injectable(self) -> bool:
        return True

    def info(self) -> MIDITempoInfo:
        return MIDITempoInfo(
            bpm=self._bpm,
            beat_counter=self._beat_counter
        )

    def set_in_port(self, port_name):
        pass

    def set_out_port(self, port_name):
        pass

    def start(self):
        self._is_running = True
        self._beat_origin = time.time()

        while self._is_running:
            self._update()
            time.sleep(0.001)

    def stop(self):
        self._is_running = False

    def send_tap(self):
        now = time.time()
        if not self._is_tapping:
            self._tap_count = 0
            self._first_tap = now

        self._latest_tap = now
        self._tap_count += 1
        self._is_tapping = True

    def _update(self):
        now = time.time()

        if self._is_tapping and self._tap_count >= 2:
            average_tap_interval = (now - self._first_tap) / self._tap_count
            since_latest_tap = now - self._latest_tap

            if since_latest_tap > average_tap_interval * 1.5:
                self._is_tapping = False

                if average_tap_interval >= self._minimum_tap_interval:
                    self._beat_origin = self._first_tap
                    self._bpm = 60 / average_tap_interval
                    self._send_bpm_to_osc()

        self._beat_counter = (now - self._beat_origin) / 60 * self._bpm

    def _send_bpm_to_osc(self):
        # TODO are we allowed to do this here ?
        Components().osc_message_sender.send(
            control_name='bpm_value',
            value=f"{self._bpm:.1f}",
            sender_ip='Server'
        )
