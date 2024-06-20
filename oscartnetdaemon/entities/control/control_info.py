from dataclasses import dataclass, field
from typing import Any

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.control.control_type_enum import ControlType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class ControlInfo:
    name: str
    type: ControlType
    values: list[Any] = field(default_factory=list)
