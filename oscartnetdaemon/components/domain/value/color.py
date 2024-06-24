from dataclasses import dataclass, field

from oscartnetdaemon.components.domain.value.abstract import AbstractValue


@dataclass
class ColorValue(AbstractValue):
    h: float = 0.0
    s: float = 0.0
    l: float = 0.0
