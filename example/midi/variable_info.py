from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.domain_contract.variable_info import VariableInfo
from oscartnetdaemon.components.new_midi.io.parsing_info import MIDIParsingInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIVariableInfo(VariableInfo):
    device_name: str
    midi_parsing: MIDIParsingInfo
