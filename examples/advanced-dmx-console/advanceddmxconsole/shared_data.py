from oscartnetdaemon.domain_contract.base_shared_data import BaseSharedData


class SharedData(BaseSharedData):
    def __init__(self):
        self.current_program_name: str = ""
        self.fixture_names: list[str] = list()

    def set_fixture_names(self, names: list[str]):
        self.fixture_names = names

    def get_fixture_names(self) -> list[str]:
        return self.fixture_names
