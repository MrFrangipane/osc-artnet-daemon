import math

from oscartnetdaemon.core.pattern.abstract import AbstractPattern


class SinPattern(AbstractPattern):
    def read_pattern(self, group_position, time_scale, beat_counter, parameter=None, playmode=0) -> float:
        return math.sin(group_position * 2. + beat_counter * time_scale)
