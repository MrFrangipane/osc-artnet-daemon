from dataclasses import dataclass


@dataclass
class Mood:
    bpm: float = 0.0
    phase: float = 0.0
    hue: float = 0.0
    saturation: float = 1.0
    value: float = 1.0
