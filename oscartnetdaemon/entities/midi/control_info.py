from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.midi.control_type_enum import MIDIControlType
from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.parsing_info import MIDIParsingInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlInfo:
    midi: MIDIParsingInfo
    name: str
    type: MIDIControlType
    device: MIDIDeviceInfo
    feedback_messages: bool = False
    layer_name: str = ""
    page: int = -1
    mapped_to: str = ""

    def __repr__(self):
        if self.mapped_to:
            return f"{self.__class__.__name__}('{self.name}' > {self.mapped_to})"
        return f"{self.__class__.__name__}('{self.name}')"
