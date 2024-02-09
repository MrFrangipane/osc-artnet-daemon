from dataclasses import dataclass


# fixme: factorize with Mapping ?
@dataclass
class Tristan200:
    pan: int = 0
    pan_fine: int = 0
    tilt: int = 0
    tilt_fine: int = 0
    moving_speed: int = 0
    color: int = 0
    gobo1: int = 0
    gobo1_rotation: int = 0
    gobo2: int = 0
    prism: int = 0
    prism_rotation: int = 0
    frost: int = 0
    focus: int = 0
    focus_fine: int = 0
    shutter: int = 0
    dimmer: int = 0
    dimmer_fine: int = 0
    reset: int = 0
