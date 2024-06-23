from dataclasses import dataclass, field
from typing import Any

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.domain.entities.control_type_enum import DomainControlType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class DomainControlInfo:
    name: str
    type: DomainControlType
    values: list[Any] = field(default_factory=list)
