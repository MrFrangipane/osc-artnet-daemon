from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.pattern.store_containers import PatternStoreContainer, PatternIndexContainer, PatternGroupPlaceContainer, PatternStepContainer
from oscartnetdaemon.core.show.item import ShowItem


class PatternStore:

    def __init__(self):
        self.data: PatternStoreContainer = PatternStoreContainer()
        self._wheel_call_back: callable = None

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

    def get_steps(self, show_item: ShowItem, pattern_index: int) -> dict[int, dict[str, int]]:
        if show_item.name not in self.data.fixture_type:
            return dict()

        if pattern_index not in self.data.fixture_type[show_item.name].pattern_index:
            return dict()

        if show_item.group_info.place not in self.data.fixture_type[show_item.name].pattern_index[pattern_index].group_place:
            return dict()

        return self.data.fixture_type[show_item.name].pattern_index[pattern_index].group_place[show_item.group_info.place].step

    def set_steps(self, show_item: ShowItem, pattern_index: int, steps: dict[dict[str, int]]):
        if show_item.name not in self.data.fixture_type:
            self.data.fixture_type[show_item.name] = PatternIndexContainer()

        if pattern_index not in self.data.fixture_type[show_item.name].pattern_index:
            self.data.fixture_type[show_item.name].pattern_index[pattern_index] = PatternGroupPlaceContainer()

        if show_item.group_info.place not in self.data.fixture_type[show_item.name].pattern_index[pattern_index].group_place:
            self.data.fixture_type[show_item.name].pattern_index[pattern_index].group_place[show_item.group_info.place] = PatternStepContainer()

        self.data.fixture_type[show_item.name].pattern_index[pattern_index].group_place[show_item.group_info.place].step = steps

    # FIXME create a PatternEditor class
    def wheel_changed(self, wheel):
        if self._wheel_call_back is not None:
            self._wheel_call_back(wheel)

    def set_wheel_callback(self, callback: callable):
        self._wheel_call_back = callback

    @staticmethod
    def set_wheel_value(value: float):
        # TODO use an API instead of Component
        if Components().osc_message_sender is None:
            return

        Components().osc_message_sender.send_to_all_raw(
            f"/#pattern_edition/wheel", value
        )

    def set_current_step(self, show_item: ShowItem, pattern_index: int, step_index: int):
        # TODO use an API instead of Component
        if Components().fixture_updater is None:
            return

        step = self.get_steps(show_item, pattern_index).get(step_index, None)
        Components().fixture_updater.set_pattern_edition_step(
            show_item=show_item,
            step=step
        )
