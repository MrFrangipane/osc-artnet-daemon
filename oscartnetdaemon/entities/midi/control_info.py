from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.parsing_info import MidiParsingInfo
from oscartnetdaemon.entities.midi.control_type_enum import MIDIControlType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlInfo:
    midi: MidiParsingInfo
    name: str
    type: MIDIControlType
    device: MIDIDeviceInfo
    feedback_message: bool = False
