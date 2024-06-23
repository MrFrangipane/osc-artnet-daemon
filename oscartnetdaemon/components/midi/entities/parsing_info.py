from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.midi.entities.message_type_enum import MIDIMessageType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIParsingInfo:
    type: MIDIMessageType
    channel: int
    note: int = -1