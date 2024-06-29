from dataclasses import dataclass, field

from oscartnetdaemon.domain_contract.value.base import BaseValue


@dataclass
class OSCMemorySlot:
    name: str
    values: dict[str, BaseValue] = field(default_factory=dict)
