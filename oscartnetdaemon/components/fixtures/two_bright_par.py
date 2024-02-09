from dataclasses import dataclass
import colorsys

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.python_extensions.math import map_to_int


class TwoBrightPar(BaseFixture):
    @dataclass
    class Mapping:
        red: int = 0
        green: int = 0
        blue: int = 0
        white: int = 0
        amber: int = 0
        uv: int = 0

    def map_to_channels(self, mood: Mood, group_position: float) -> list[int]:
        offset = ((group_position * 2) - 1) * mood.animation * 0.5
        hue = (mood.palette + offset) % 1.0
        red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

        mapping = TwoBrightPar.Mapping()
        mapping.red = map_to_int(red)
        mapping.green = map_to_int(green)
        mapping.blue = map_to_int(blue)

        return list(vars(mapping).values())
