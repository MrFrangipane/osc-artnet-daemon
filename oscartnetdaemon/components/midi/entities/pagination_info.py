from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIPaginationInfo:
    name: str
    left: MIDIControlInfo
    right: MIDIControlInfo
    page_count: int
    controls: list[MIDIControlInfo] = field(default_factory=list)
