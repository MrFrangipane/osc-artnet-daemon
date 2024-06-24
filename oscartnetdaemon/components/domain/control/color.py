from dataclasses import dataclass, field

from oscartnetdaemon.components.domain.control.abstract import AbstractDomainControl
from oscartnetdaemon.components.domain.value.color import ColorValue


@dataclass
class ColorControl(AbstractDomainControl):
    value: ColorValue = field(default_factory=ColorValue)
