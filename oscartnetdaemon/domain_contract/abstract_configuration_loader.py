from abc import ABC, abstractmethod

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


class AbstractConfigurationLoader(ABC):

    def __init__(self, filepaths: list[str]):
        self.filepaths = filepaths

    @abstractmethod
    def load(self) -> BaseConfiguration:
        pass
