from dataclasses import dataclass


@dataclass
class Mood:
    bpm: float = 0.0
    beat_counter: float = 0.0

    bpm_scale: int = 2  # fixme: we need an interop service between tosc and mood
    hue: float = 0.0
    palette: int = 0
    pattern: int = 0

    pattern_parameter: float = 0.0
    pattern_playmode: int = 0
    
    on_octo: float = 1.0
    on_lyre: float = 1.0
    on_wash: float = 1.0
    on_par: float = 1.0

    colorize_octo: float = 1.0
    colorize_lyre: float = 1.0
    colorize_wash: float = 1.0
    colorize_par: float = 1.0

    on_smoke: float = 0.0
    on_white: float = 0.0
    on_strobe: float = 0.0

    master_dimmer: float = 1.0
    recallable_dimmer: float = 1.0

    beam_shape: int = 0

    autoplay_on: float = 0.0
    autoplay_interval: int = 0
    autoplay_current: int = -1
