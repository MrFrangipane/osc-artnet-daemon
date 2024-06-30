from abc import ABC, abstractmethod

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


class AbstractConfigurationLoader(ABC):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    @abstractmethod
    def load(self) -> BaseConfiguration:
        pass
