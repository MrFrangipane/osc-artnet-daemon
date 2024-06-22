from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIDeviceInfo:
    name: str
    in_port_name: str
    out_port_name: str
