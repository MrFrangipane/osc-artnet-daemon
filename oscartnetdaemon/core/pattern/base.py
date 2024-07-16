class BasePattern:
    def read_pattern(self, group_position, time_scale, beat_counter, parameter=None) -> float:
        raise NotImplementedError("You have to inherit from BasePattern and override this method!")
