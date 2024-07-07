from oscartnetdaemon.components.midi.compliance_checker import MIDIComplianceChecker
from oscartnetdaemon.components.midi.io.message import MIDIMessage
from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class MIDIIndicator(VariableFloat):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: MIDIVariableInfo = self.info  # FIXME type hint for autocompletion
        value: float = self.value.value

        if MIDIComplianceChecker.with_current_layer(info) and MIDIComplianceChecker.with_current_page(info):
            self.io_message_queue_out.put(MIDIMessage(
                channel=info.midi_parsing.channel,
                device_name=info.device_name,
                type=MIDIMessageType.NoteOn,
                note=info.midi_parsing.note,
                velocity=int(self.value.value * 127)
            ))

    def handle_io_message(self, message: MIDIMessage):
        """
        From IO to ChangeNotification
        """
        pass
