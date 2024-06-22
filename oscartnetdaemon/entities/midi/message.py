from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.message_type_enum import MIDIMessageType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIMessage:
    channel: int
    device: MIDIDeviceInfo
    raw_message: Any  # Used by implementation, will probably disappear when implementing midi out
    type: MIDIMessageType
    note: int | None = None
    pitch: int | None = None
    velocity: int | None = None
