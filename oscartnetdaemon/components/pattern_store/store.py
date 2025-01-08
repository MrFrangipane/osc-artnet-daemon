from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.pattern.store_containers import (
    PatternStoreContainer, PatternIndexContainer, PatternGroupPlaceContainer, PatternStepContainer)


class PatternStore:

    def __init__(self):
        self.data: PatternStoreContainer = PatternStoreContainer()

    def get_step_while_playing(self, fixture_type: str, group_place: int) -> dict[str, int]:
        beat_counter = Components().midi_tempo.beat_counter
        mood = Components().osc_state_model.mood
        beat = beat_counter * [.25, .5, 1.0, 2.0, 4.0][mood.bpm_scale]
        pattern_index = mood.pattern

        if fixture_type not in self.data.fixture_type:
            return dict()

        if pattern_index not in self.data.fixture_type[fixture_type].pattern_index:
            return dict()

        if group_place not in self.data.fixture_type[fixture_type].pattern_index[pattern_index].group_place:
            return dict()

        pattern = self.data.fixture_type[fixture_type].pattern_index[pattern_index].group_place[group_place]
        if not pattern.step:
            return dict()

        # TODO call @diffty's interpolation

        return pattern.step.get(int(beat) % len(pattern.step), dict())

    def get_steps(self, fixture_type: str, pattern_index: int, group_place: int) -> dict[int, dict[str, int]]:
        if fixture_type not in self.data.fixture_type:
            return dict()

        if pattern_index not in self.data.fixture_type[fixture_type].pattern_index:
            return dict()

        if group_place not in self.data.fixture_type[fixture_type].pattern_index[pattern_index].group_place:
            return dict()

        return self.data.fixture_type[fixture_type].pattern_index[pattern_index].group_place[group_place].step

    def set_steps(self, fixture_type: str, pattern_index: int, group_place: int, steps: dict[dict[str, int]]):
        if fixture_type not in self.data.fixture_type:
            self.data.fixture_type[fixture_type] = PatternIndexContainer()

        if pattern_index not in self.data.fixture_type[fixture_type].pattern_index:
            self.data.fixture_type[fixture_type].pattern_index[pattern_index] = PatternGroupPlaceContainer()

        if group_place not in self.data.fixture_type[fixture_type].pattern_index[pattern_index].group_place:
            self.data.fixture_type[fixture_type].pattern_index[pattern_index].group_place[group_place] = PatternStepContainer()

        self.data.fixture_type[fixture_type].pattern_index[pattern_index].group_place[group_place].step = steps
