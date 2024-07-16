from dataclasses import dataclass


@dataclass
class Mood:
    bpm: float = 0.0
    beat_counter: float = 0.0

    blinking: float = 0.5
    bpm_scale: int = 2  # fixme: we need an interop service between tosc and mood
    hue: float = 0.0
    palette: int = 0
    pattern: int = 0
    texture: float = 0.5

    pattern_parameter: float = 0.0
    pattern_playmode: int = 0
    
    on_octo: float = 1.0
    on_lyre: float = 1.0
    on_wash: float = 1.0
    on_par: float = 1.0

    master_dimmer: float = 1.0
    recallable_dimmer: float = 1.0
