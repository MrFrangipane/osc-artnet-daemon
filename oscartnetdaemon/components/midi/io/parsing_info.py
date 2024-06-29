from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIParsingInfo:
    type: MIDIMessageType
    channel: int = -1
    note: int = -1
    bytes_as_str: list[str] | None = None
