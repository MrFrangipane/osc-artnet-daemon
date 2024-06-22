from oscartnetdaemon.components.midi.controls.abstract import MIDIAbstractControl
from oscartnetdaemon.entities.midi.context import MIDIContext
from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.control_update_info import MIDIControlUpdateInfo
from oscartnetdaemon.entities.midi.message import MIDIMessage


class MIDIToggleControl(MIDIAbstractControl):

    def __init__(self, info: MIDIControlInfo):
        super().__init__(info)
        self.value = 0.0

    def handle_message(self, message: MIDIMessage, context: MIDIContext) -> None | MIDIControlUpdateInfo:
        if message.velocity == 127:
            self.value = float(not bool(self.value))
            return MIDIControlUpdateInfo(
                control_name=self.info.name,
                value=self.value
            )
