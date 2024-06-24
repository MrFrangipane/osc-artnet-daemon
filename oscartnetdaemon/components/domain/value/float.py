from dataclasses import dataclass

from oscartnetdaemon.components.domain.value.abstract import AbstractValue


@dataclass
class FloatValue(AbstractValue):
    value: float = 0.0
