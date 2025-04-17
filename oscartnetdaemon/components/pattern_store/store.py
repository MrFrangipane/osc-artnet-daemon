from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.pattern.store_containers import PatternStoreContainer, PatternIndexContainer, PatternGroupPlaceContainer, PatternStepContainer
from oscartnetdaemon.core.show.item_info import ShowItemInfo

def _lerp_dict(a: dict, b: dict, factor: float) -> dict:
    keys = set(a.keys()).union(b.keys())

    return {
        key: int(float(a.get(key, 0)) * (1 - factor)) + int(float(b.get(key, 0)) * factor)
        if a.get(key, 0) != b.get(key, 0) else b.get(key, 0)
        for key in keys
    }


def _stretch_time(time: float, factor: float) -> float:
    if factor == 0.0:
        return 0.0

    if time >= factor:
        return 1.0

    return time / factor


class PatternStore:

    def __init__(self):
        self.data: PatternStoreContainer = PatternStoreContainer()
        self._wheel_call_back: callable = None

    def get_step_while_playing(self, fixture_type: str, group_place: int) -> dict[str, int]:
        tempo = Components().midi_tempo.info()
        mood = Components().osc_state_model.mood
        beat = tempo.beat_counter * [.25, .5, 1.0, 2.0, 4.0][mood.bpm_scale]
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

        #
        # Interpolation
        step_id = int(beat) % len(pattern.step)
        next_step_id = (step_id + 1) % len(pattern.step)

        step = pattern.step.get(step_id, dict())
        next_step = pattern.step.get(next_step_id, dict())
        factor = _stretch_time(beat - int(beat), mood.pattern_parameter)
        return _lerp_dict(step, next_step, factor)

    def get_steps(self, show_item_info: ShowItemInfo, pattern_index: int) -> dict[int, dict[str, int]]:
        if show_item_info.name not in self.data.fixture_type:
            return dict()

        if pattern_index not in self.data.fixture_type[show_item_info.name].pattern_index:
            return dict()

        if show_item_info.group_info.place not in self.data.fixture_type[show_item_info.name].pattern_index[pattern_index].group_place:
            return dict()

        return self.data.fixture_type[show_item_info.name].pattern_index[pattern_index].group_place[show_item_info.group_info.place].step

    def set_steps(self, show_item_info: ShowItemInfo, pattern_index: int, steps: dict[int, dict[str, int]]):
        if show_item_info.name not in self.data.fixture_type:
            self.data.fixture_type[show_item_info.name] = PatternIndexContainer()

        if pattern_index not in self.data.fixture_type[show_item_info.name].pattern_index:
            self.data.fixture_type[show_item_info.name].pattern_index[pattern_index] = PatternGroupPlaceContainer()

        if show_item_info.group_info.place not in self.data.fixture_type[show_item_info.name].pattern_index[pattern_index].group_place:
            self.data.fixture_type[show_item_info.name].pattern_index[pattern_index].group_place[show_item_info.group_info.place] = PatternStepContainer()

        self.data.fixture_type[show_item_info.name].pattern_index[pattern_index].group_place[show_item_info.group_info.place].step = steps

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

    def set_current_step(self, show_item_info: ShowItemInfo, pattern_index: int, step_index: int):
        # TODO use an API instead of Component
        if Components().fixture_updater is None:
            return

        step = self.get_steps(show_item_info, pattern_index).get(step_index, None)
        Components().fixture_updater.set_pattern_edition_step(
            show_item_info=show_item_info,
            step=step
        )

    def pattern_names(self) -> list[str]:
        return self.data.pattern_names

    def set_pattern_name(self, pattern_index: int, name: str) -> None:
        self.data.pattern_names[pattern_index] = name

    def shift_steps(self, show_item_info: ShowItemInfo, pattern_index: int, offset: int) -> None:
        steps = self.get_steps(show_item_info, pattern_index)
        if not steps:
            return

        new_steps = dict()
        for step_index in range(len(steps)):
            new_steps[step_index] = steps[(step_index - offset) % len(steps)]

        self.set_steps(show_item_info, pattern_index, new_steps)
