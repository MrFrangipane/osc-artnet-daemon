from oscartnetdaemon.core.components import Components


class PatternStoreAPI:

    @staticmethod
    def get_step_while_playing(fixture_type: str, group_place: int) -> dict[str, int]:
        return Components().pattern_store.get_step_while_playing(fixture_type, group_place)

    @staticmethod
    def get_pattern(fixture_type: str, group_place: int, pattern_index: int) -> list[dict[str, int]]:
        return Components().pattern_store.get_pattern(fixture_type, group_place, pattern_index)

    @staticmethod
    def set_pattern(fixture_type: str, group_place: int, pattern_index: int, pattern: list[dict[str, int]]):
        Components().pattern_store.set_pattern(fixture_type, group_place, pattern_index, pattern)
