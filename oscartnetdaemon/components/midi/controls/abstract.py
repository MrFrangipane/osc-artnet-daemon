from abc import ABC, abstractmethod

from oscartnetdaemon.entities.midi.context import MIDIContext
from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.control_update_info import MIDIControlUpdateInfo
from oscartnetdaemon.entities.midi.message import MIDIMessage
from oscartnetdaemon.entities.midi.message_type_enum import MIDIMessageType


class MIDIAbstractControl(ABC):

    def __init__(self, info: MIDIControlInfo):
        self.info = info

    def complies_with(self, message: MIDIMessage, context: MIDIContext):
        channel_ok = self.info.midi.channel == message.channel
        device_ok = self.info.device == message.device
        layer_ok = self.info.layer_name == "" or self.info.layer_name == context.current_layer.name
        page_ok = self.info.page == -1 or self.info.page == context.current_page
        type_ok = message.type == self.info.midi.type

        if not device_ok or not type_ok or not page_ok or not layer_ok or not channel_ok:
            return False

        compliant = {
            MIDIMessageType.NoteOn: message.note == self.info.midi.note,
            MIDIMessageType.PitchWheel: True
        }
        return compliant[message.type]

    @abstractmethod
    def handle_message(self, message: MIDIMessage, context: MIDIContext) -> None | MIDIControlUpdateInfo:
        pass
