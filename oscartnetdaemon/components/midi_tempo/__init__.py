import logging
import time

import mido

from oscartnetdaemon.core.midi_tempo_info import MIDITempoInfo

_logger = logging.getLogger(__name__)


class MIDITempo:
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
        _logger.info(f"MIDI service starting (in='{self._port_in_name}' out='{self._port_out_name}')")

        try:
            self._out = mido.open_output(self._port_out_name)
        except OSError:
            # available_out_ports = mido.get_output_names()  # todo message log
            _logger.warning(f"MIDI out port '{self._port_out_name}' not found")
            _logger.warning(f"Falling back to fixed 120 bpm tempo")
            self._fallback_loop()
            return

        try:
            self._in = mido.open_input(self._port_in_name)
        except OSError:
            # available_in_ports = mido.get_input_names()  # todo message log
            _logger.warning(f"MIDI in port '{self._port_in_name}' not found")
            _logger.warning(f"Falling back to fixed 120 bpm tempo")
            self._fallback_loop()
            return

        self._midi_loop()

    def _midi_loop(self):
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

    def _fallback_loop(self):
        timestamp = time.time()
        self.beat_counter = 0
        self.bpm = 120

        self._is_running = True
        while self._is_running:
            time_interval = time.time() - timestamp
            timestamp = time.time()
            self.beat_counter += time_interval * self.bpm / 60.0

            # todo: can we do better ?
            if time.time() - self._latest_tap > 5 and self._is_tapping:
                self._is_tapping = False

            time.sleep(0.001)

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
