from oscartnetdaemon.components.domain.value.float import FloatValue
from oscartnetdaemon.components.midi.controls.abstract import MIDIAbstractControl
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo
from oscartnetdaemon.components.midi.entities.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.entities.message import MIDIMessage
from oscartnetdaemon.components.midi.entities.message_type_enum import MIDIMessageType


class MIDIButtonControl(MIDIAbstractControl):

    def __init__(self, info: MIDIControlInfo):
        super().__init__(info)
        self.value: FloatValue = FloatValue()

    def handle_message(self, message: MIDIMessage, context: MIDIContext) -> bool:
        self.value.value = float(message.velocity) / 127.0
        return True

    def make_message(self) -> MIDIMessage:
        return MIDIMessage(
            channel=self.info.midi.channel,
            device=self.info.device,
            type=MIDIMessageType.NoteOn,
            note=self.info.midi.note,
            velocity=int(self.value.value * 127)
        )
