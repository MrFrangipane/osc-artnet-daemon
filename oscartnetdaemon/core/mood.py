from dataclasses import dataclass


@dataclass
class Mood:
    animation: float = 0.5
    blinking: float = 0.5
    bpm: float = 0.0
    bpm_scale: int = 1
    palette: float = 0.0
    palette_animation: int = 2
    texture: float = 0.5
