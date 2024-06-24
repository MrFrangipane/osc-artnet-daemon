from dataclasses import dataclass, field

from oscartnetdaemon.components.domain.value.abstract import AbstractValue
from oscartnetdaemon.components.domain.entities.control_info import DomainControlInfo


@dataclass
class AbstractDomainControl:
    info: DomainControlInfo
    value: AbstractValue = field(default_factory=AbstractValue)
