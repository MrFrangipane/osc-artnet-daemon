from oscartnetdaemon.core.components import Components


class PatternStore:

    def __init__(self):
        self.data: dict[str, list[list[list[dict[str, int]]]]] = dict()

    def get_step_while_playing(self, fixture_type: str, group_place: int) -> dict[str, int]:
        beat_counter = Components().midi_tempo.beat_counter
        mood = Components().osc_state_model.mood
        beat = beat_counter * [.25, .5, 1.0, 2.0, 4.0][mood.bpm_scale]
        pattern_index = mood.pattern

        pattern = self.data[fixture_type][pattern_index][group_place]
        if not pattern:
            return {}

        return pattern[int(beat) % len(pattern)]

    def get_pattern(self, fixture_type: str, group_place: int, pattern_index: int) -> list[dict[str, int]]:
        if fixture_type not in self.data:
            return []

        return self.data[fixture_type][pattern_index][group_place]

    def set_pattern(self, fixture_type: str, group_place: int, pattern_index: int, pattern: list[dict[str, int]]):
        self.data[fixture_type][pattern_index][group_place] = pattern
