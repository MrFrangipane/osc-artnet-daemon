from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.domain_contract.variable_info import VariableInfo
from oscartnetdaemon.components.new_midi.io.parsing_info import MIDIParsingInfo
from oscartnetdaemon.components.new_midi.page_direction_enum import MIDIPageDirection


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIVariableInfo(VariableInfo):
    device_name: str
    midi_parsing: MIDIParsingInfo
    page_number: int = -1
    is_page_button: bool = False
    pagination_name: str = ""
    page_direction: MIDIPageDirection = MIDIPageDirection.Up
