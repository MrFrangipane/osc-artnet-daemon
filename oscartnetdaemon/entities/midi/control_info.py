from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.parsing_info import MIDIParsingInfo
from oscartnetdaemon.entities.midi.control_type_enum import MIDIControlType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlInfo:
    midi: MIDIParsingInfo
    name: str
    type: MIDIControlType
    device: MIDIDeviceInfo
    feedback_messages: bool = False
