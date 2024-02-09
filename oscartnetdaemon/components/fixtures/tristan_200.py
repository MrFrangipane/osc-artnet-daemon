import math
import time
from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood


class Tristan200(BaseFixture):
    @dataclass
    class Mapping:
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

    def map_to_channels(self, mood: Mood, group_position: float) -> list[int]:
        mapping = Tristan200.Mapping()
        mapping.color = int(mood.palette * 255)
        mapping.pan = int(((math.cos(time.time()) * 0.5) + 0.5) * 255)
        mapping.tilt = int(mood.texture * 255)

        return list(vars(mapping).values())
