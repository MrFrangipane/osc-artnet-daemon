from oscartnetdaemon.core.pattern.base import BasePattern


class RisePattern(BasePattern):
    def read_pattern(self, group_position, time_scale, beat_counter, parameter=None) -> float:
        return (beat_counter * time_scale) % 1.
