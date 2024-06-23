from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.midi.entities.control_type_enum import MIDIControlType
from oscartnetdaemon.components.midi.entities.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.entities.parsing_info import MIDIParsingInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIControlInfo:
    midi: MIDIParsingInfo
    name: str
    type: MIDIControlType
    device: MIDIDeviceInfo
    layer_name: str = ""
    page: int = -1
    mapped_to: str = ""

    def __repr__(self):
        if self.mapped_to:
            return f"{self.__class__.__name__}('{self.name}' > {self.mapped_to})"
        return f"{self.__class__.__name__}('{self.name}')"