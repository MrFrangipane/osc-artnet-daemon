from oscartnetdaemon.components.domain.value.float import FloatValue
from oscartnetdaemon.components.midi.controls.abstract import MIDIAbstractControl
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo
from oscartnetdaemon.components.midi.entities.message import MIDIMessage


class MIDIFaderControl(MIDIAbstractControl):

    def __init__(self, info: MIDIControlInfo):
        super().__init__(info)
        self.value: FloatValue = FloatValue()

    def handle_message(self, message: MIDIMessage, context: MIDIContext) -> bool:
        self.value.value = float(message.pitch + 8192) / 16380.0
        return True

    def make_message(self) -> MIDIMessage:
        return MIDIMessage(
            channel=self.info.midi.channel,
            device=self.info.device,
            type=self.info.midi.type,
            pitch=int(self.value.value * 16380.0 - 8192)
        )
