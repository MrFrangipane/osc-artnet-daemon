from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlLayerInfo:
    name: str
    trigger: MIDIControlInfo
