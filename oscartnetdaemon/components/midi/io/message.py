from dataclasses import dataclass

from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage


@dataclass
class MIDIMessage(AbstractIOMessage):  # TODO: do we need to inherit from AbstractIOMessage (and get .info ?) ?
    device_name: str
    type: MIDIMessageType
    channel: int | None = None
    note: int | None = None
    pitch: int | None = None
    velocity: int | None = None
    data: bytes | None = None
