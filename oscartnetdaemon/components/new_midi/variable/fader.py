from oscartnetdaemon.components.new_midi.compliance_checker import MIDIComplianceChecker
from oscartnetdaemon.components.new_midi.io.message import MIDIMessage
from oscartnetdaemon.components.new_midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class MIDIFader(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: MIDIVariableInfo = self.info  # FIXME type hint for autocompletion
        if MIDIComplianceChecker.with_current_layer(info) and MIDIComplianceChecker.with_current_page(info):
            self.io_message_queue_out.put(MIDIMessage(
                channel=info.midi_parsing.channel,
                device_name=info.device_name,
                type=MIDIMessageType.PitchWheel,
                pitch=int(self.value.value * 16380.0 - 8192)
            ))

    def handle_io_message(self, message: MIDIMessage):
        """
        From IO to ChangeNotification
        """
        if not MIDIComplianceChecker.with_io_message(self.info, message):
            return

        self.value.value = float(message.pitch + 8192) / 16380.0
        self.notify_change()
