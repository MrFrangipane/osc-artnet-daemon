from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, LetterCase


from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlLayerInfo:
    name: str
    trigger: MIDIControlInfo
    controls: list[MIDIControlInfo] = field(default_factory=list)
