from oscartnetdaemon.domain_contract.base_shared_data import BaseSharedData


class ArtnetSharedData(BaseSharedData):
    def __init__(self):
        self.current_program_name: str = ""
        self.fixture_names: list[str] = list()
        self.selected_fixture_index: int = -1
        self.has_current_program_changed: bool = False

    def set_has_current_program_changed(self, has_changed: bool):
        self.has_current_program_changed = has_changed

    def get_has_current_program_changed(self) -> bool:
        return self.has_current_program_changed

    def set_current_program_name(self, name: str):
        self.current_program_name = name

    def get_current_program_name(self) -> str:
        return self.current_program_name

    def set_fixture_names(self, names: list[str]):
        self.fixture_names = names

    def get_fixture_names(self) -> list[str]:
        return self.fixture_names

    def set_selected_fixture_index(self, index: int):
        self.selected_fixture_index = index

    def get_selected_fixture_index(self) -> int:
        return self.selected_fixture_index
