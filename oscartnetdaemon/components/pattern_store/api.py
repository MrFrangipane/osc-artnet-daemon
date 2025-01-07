from oscartnetdaemon.core.components import Components


class PatternStoreAPI:

    @staticmethod
    def get_step(fixture_type: str, group_place: int) -> dict[str, int]:
        return Components().pattern_store.get_step(fixture_type, group_place)
