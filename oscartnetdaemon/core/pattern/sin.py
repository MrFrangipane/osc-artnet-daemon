import math

from oscartnetdaemon.core.pattern.base import BasePattern


class SinPattern(BasePattern):
    def read_pattern(self, group_position, time_scale, beat_counter, parameter=None) -> float:
        return math.sin(group_position * 2. + beat_counter * time_scale)
