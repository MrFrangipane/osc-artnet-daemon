from dataclasses import dataclass, field

from oscartnetdaemon.components.domain.control.abstract import AbstractDomainControl
from oscartnetdaemon.components.domain.value.float import FloatValue


@dataclass
class FloatControl(AbstractDomainControl):
    value: FloatValue = field(default_factory=FloatValue)
