from oscartnetdaemon.core.components import Components


class PatternStoreAPI:

    @staticmethod
    def get_step_while_playing(fixture_type: str, group_place: int) -> dict[str, int]:
        return Components().pattern_store.get_step_while_playing(
            fixture_type=fixture_type,
            group_place=group_place
        )

    @staticmethod
    def get_steps(fixture_type: str, pattern_index: int, group_place: int) -> dict[int, dict[str, int]]:
        return Components().pattern_store.get_steps(
            fixture_type=fixture_type,
            pattern_index=pattern_index,
            group_place=group_place
        )

    @staticmethod
    def set_steps(fixture_type: str, pattern_index: int, group_place: int, steps: dict[int, dict[str, int]]):
        Components().pattern_store.set_steps(
            fixture_type=fixture_type,
            pattern_index=pattern_index,
            group_place=group_place,
            steps=steps
        )
