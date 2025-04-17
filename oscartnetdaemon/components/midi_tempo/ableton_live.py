import logging
import time

import mido

from oscartnetdaemon.components.midi_tempo.abstract import AbstractMIDITempo
from oscartnetdaemon.core.midi_tempo_info import MIDITempoInfo


_logger = logging.getLogger(__name__)


class AbletonLiveMidiTempo(AbstractMIDITempo):
    BeatTickCount = 24

    def __init__(self):
        self._port_in_name: str = None
        self._port_out_name: str = None
        self._is_running: bool = False

        self._out: mido.ports.IOPort = None
        self._in: mido.ports.IOPort = None

        self._is_tapping = False
        self._latest_tap = time.time()
        self.beat_counter: float = 0
        self.bpm = 0

    def is_injectable(self) -> bool:
        try:
            self._out = mido.open_output(self._port_out_name)
            self._in = mido.open_input(self._port_in_name)
        except OSError:
            return False

        return True

    def info(self) -> MIDITempoInfo:
        return MIDITempoInfo(
            beat_counter=self.beat_counter,
            bpm=self.bpm
        )

    def set_in_port(self, port_name):
        self._port_in_name = port_name

    def set_out_port(self, port_name):
        self._port_out_name = port_name

    def start(self):
        _logger.info(f"Ableton Live MIDI tempo service starting (in='{self._port_in_name}' out='{self._port_out_name}')")

        if self._out is None or self._in is None:
            raise RuntimeError("MIDI service not injected")

        self._loop()

    def _loop(self):
        timestamp = time.time()
        message_count = 0
        self.beat_counter = 0

        self._is_running = True
        while self._is_running:
            message = self._in.poll()
            if message is None or message.type != "clock":
                time.sleep(0.001)
                continue

            message_count += 1
            self.beat_counter += 1.0 / self.BeatTickCount
            if message_count > self.BeatTickCount:
                time_interval = time.time() - timestamp
                timestamp = time.time()
                message_count = 0
                self.bpm = 60.0 / time_interval

            # todo: can we do better ?
            if time.time() - self._latest_tap > 5 and self._is_tapping:
                self._is_tapping = False

            time.sleep(0.001)

        self._out.close()
        self._out = None

        self._in.close()
        self._in = None

        _logger.info(f"MIDI service stopped")

    def stop(self):
        self._is_running = False

    def send_tap(self):
        # todo: can we do better ?
        self._latest_tap = time.time()
        if not self._is_tapping:
            self.beat_counter = 0
            self._is_tapping = True
        else:
            self.beat_counter += 1

        if self._out is None:
            return

        self._out.send(mido.Message('note_on', note=60))
        self._out.send(mido.Message('note_off', note=60))
