from dataclasses import dataclass


@dataclass
class MIDITempoInfo:
    bpm: float
    beat_counter: float
