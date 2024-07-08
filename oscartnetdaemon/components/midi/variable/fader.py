from oscartnetdaemon.components.midi.compliance_checker import MIDIComplianceChecker
from oscartnetdaemon.components.midi.io.message import MIDIMessage
from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class MIDIFader(VariableFloat):

    def __init__(self, info: "VariableInfo", io_message_queue_out: "Queue[AbstractIOMessage]", notification_queue_out: "Queue[ChangeNotification]"):
        super().__init__(info, io_message_queue_out, notification_queue_out)
        self.is_touch: bool = False

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        if self.is_touch:
            return

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
        if MIDIComplianceChecker.with_io_message(self.info, message):
            self.value.value = float(message.pitch + 8192) / 16380.0
            self.notify_change()

        if MIDIComplianceChecker.with_io_message_and_parsing(self.info, self.info.midi_touch, message):
            self.is_touch = bool(message.velocity)
            self.notify_change()
