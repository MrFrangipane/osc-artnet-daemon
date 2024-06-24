from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.midi.entities.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.entities.message_type_enum import MIDIMessageType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class MIDIMessage:
    channel: int
    device: MIDIDeviceInfo
    type: MIDIMessageType
    note: int | None = None
    pitch: int | None = None
    velocity: int | None = None
