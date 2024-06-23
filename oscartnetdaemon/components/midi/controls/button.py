from oscartnetdaemon.components.midi.controls.abstract import MIDIAbstractControl
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.control_info import MIDIControlInfo
from oscartnetdaemon.components.midi.entities.message import MIDIMessage


class MIDIButtonControl(MIDIAbstractControl):

    def __init__(self, info: MIDIControlInfo):
        super().__init__(info)

    def handle_message(self, message: MIDIMessage, context: MIDIContext) -> bool:
        self.value = float(message.velocity) / 127.0
        return True
