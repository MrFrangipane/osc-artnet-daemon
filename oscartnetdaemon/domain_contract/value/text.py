from dataclasses import dataclass
from oscartnetdaemon.domain_contract.value.base import BaseValue


@dataclass
class ValueText(BaseValue):
    value: str = ""

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.value})>"
