import mido
import time

from oscartnetdaemon.core.midi_tempo_info import MIDITempoInfo


class MIDITempo:
    BeatTickCount = 24

    def __init__(self):
        self._port_name: str = None
        self._is_running: bool = False

        self.beat_counter: float = 0
        self.bpm = 0

    @property
    def available_ports(self) -> list[str]:
        return mido.get_input_names()

    def info(self) -> MIDITempoInfo:
        return MIDITempoInfo(
            beat_counter=self.beat_counter,
            bpm=self.bpm
        )

    def set_port(self, port_name):
        self._port_name = port_name

    def start(self):
        timestamp = time.time()
        message_count = 0
        self.beat_counter = 0

        self._is_running = True
        with mido.open_input(self._port_name) as input_port:
            for message in input_port:
                if not self._is_running:
                    return

                if message.type != "clock":
                    continue

                message_count += 1
                self.beat_counter += 1.0 / self.BeatTickCount
                if message_count > self.BeatTickCount:
                    time_interval = time.time() - timestamp
                    timestamp = time.time()
                    message_count = 0
                    self.bpm = 60.0 / time_interval

    def stop(self):
        self._is_running = False
