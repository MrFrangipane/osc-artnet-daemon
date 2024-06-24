from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlUpdateInfo:
    control_name: str
    mapped_to: str
    value: Any
