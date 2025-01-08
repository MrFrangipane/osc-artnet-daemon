from abc import ABC, abstractmethod


class AbstractPattern(ABC):

    @abstractmethod
    def read_pattern(self, group_position, time_scale, beat_counter, parameter=None, playmode=0) -> float:
        pass
