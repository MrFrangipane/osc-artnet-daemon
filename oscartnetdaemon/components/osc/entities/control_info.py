from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.osc.entities.control_type_enum import OSCControlType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCControlInfo:
    caption: str
    type: OSCControlType
    osc_address: str
    labels: list[str] = field(default_factory=list)
    mapped_to: str = ""
