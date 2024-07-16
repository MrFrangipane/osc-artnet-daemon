import math
from typing import List

from oscartnetdaemon.core.pattern.base import BasePattern


class SequencePattern(BasePattern):
    def __init__(self, *pattern_array: List[List[int]]):
        self.pattern_array = pattern_array
    
    def read_pattern(self, group_position, time_scale, beat_counter, parameter=0.) -> float:
        smooth = parameter
        
        beat_counter = beat_counter * time_scale
        f_group_index = (len(self.pattern_array) - 1) * group_position

        # how expensive is that ?
        group_index = math.ceil(f_group_index) if f_group_index % 1 >= 0.5 else int(f_group_index)

        pattern_index = int(beat_counter % len(self.pattern_array[group_index]))
        pattern_value = self.pattern_array[group_index][pattern_index]

        if smooth > 0:
            nb_patterns = len(self.pattern_array[group_index])

            prev_pattern_index = math.floor(beat_counter % nb_patterns)
            next_pattern_index = math.ceil(beat_counter % nb_patterns)

            if next_pattern_index > nb_patterns-1:
                next_pattern_index = 0
            
            prev_pattern_value = self.pattern_array[group_index][prev_pattern_index]
            next_pattern_value = self.pattern_array[group_index][next_pattern_index]

            pattern_index_modulo = beat_counter % 1.
            pattern_smooth_value = (next_pattern_value - prev_pattern_value) * pattern_index_modulo + prev_pattern_value

            pattern_value = pattern_value + (pattern_smooth_value - pattern_value) * smooth

        return pattern_value


