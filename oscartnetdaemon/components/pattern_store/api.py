from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.pattern.store_containers import PatternStepContainer
from oscartnetdaemon.core.show.item_info import ShowItemInfo


class PatternStoreAPI:

    @staticmethod
    def get_step_while_playing(fixture_type: str, group_place: int) -> dict[str, int]:
        return Components().pattern_store.get_step_while_playing(
            fixture_type=fixture_type,
            group_place=group_place
        )

    @staticmethod
    def get_step_container(show_item_info: ShowItemInfo, pattern_index: int) -> PatternStepContainer | None:
        return Components().pattern_store.get_step_container(
            show_item_info=show_item_info,
            pattern_index=pattern_index
        )

    @staticmethod
    def set_steps(show_item_info: ShowItemInfo, pattern_index: int, steps: dict[int, dict[str, int]], inverted_keys: list[str]):
        Components().pattern_store.set_steps(
            show_item_info=show_item_info,
            pattern_index=pattern_index,
            steps=steps,
            inverted_keys=inverted_keys
        )

    @staticmethod
    def set_wheel_callback(callback: callable):
        Components().pattern_store.set_wheel_callback(callback)

    @staticmethod
    def set_wheel_value(value: float):
        Components().pattern_store.set_wheel_value(value)

    @staticmethod
    def set_current_step(show_item_info: ShowItemInfo, pattern_index: int, step_index: int):
        Components().pattern_store.set_current_step(
            show_item_info=show_item_info,
            pattern_index=pattern_index,
            step_index=step_index
        )

    @staticmethod
    def pattern_names() -> list[str]:
        return Components().pattern_store.pattern_names()

    @staticmethod
    def set_pattern_name(pattern_index: int, name: str) -> None:
        Components().pattern_store.set_pattern_name(pattern_index=pattern_index, name=name)

        # FIXME create OSCAPI ?
        if Components().osc_message_sender is None:
            return
        Components().osc_message_sender.send_pattern_names_to_all()

    @staticmethod
    def shift_steps(show_item_info: ShowItemInfo, pattern_index: int, offset: int) -> None:
        Components().pattern_store.shift_steps(show_item_info=show_item_info, pattern_index=pattern_index, offset=offset)

    @staticmethod
    def set_current_pattern(pattern_index: int):
        # FIXME very hacky !!
        if Components().osc_message_sender is not None:
            Components().osc_state_model.mood.pattern = pattern_index
            Components().osc_message_sender.send_mood_to_all()
