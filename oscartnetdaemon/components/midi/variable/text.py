from oscartnetdaemon.components.midi.compliance_checker import MIDIComplianceChecker
from oscartnetdaemon.components.midi.io.message import MIDIMessage
from oscartnetdaemon.components.midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.text import VariableText


class MIDIText(VariableText):

    def __init__(self, info: MIDIVariableInfo, io_message_queue_out: "Queue[AbstractIOMessage]", notification_queue_out: "Queue[ChangeNotification]"):
        super().__init__(info, io_message_queue_out, notification_queue_out)
        self.len: int = len(self.info.midi_parsing.bytes_as_str)  # FIXME count only number of {X} fields

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: MIDIVariableInfo = self.info  # FIXME type hint for autocompletion
        if MIDIComplianceChecker.with_current_layer(info) and MIDIComplianceChecker.with_current_page(info):
            self.io_message_queue_out.put(MIDIMessage(
                device_name=info.device_name,
                type=MIDIMessageType.SysEx,
                data=self.make_bytes()
            ))

    def handle_io_message(self, message: MIDIMessage):
        """
        From IO to ChangeNotification
        """
        if not MIDIComplianceChecker.with_io_message(self.info, message):
            return

    def make_bytes(self) -> bytes:
        # FIXME be more efficient
        chars = [" "] * self.len
        for char_number in range(min(self.len, len(self.value.value))):
            chars[char_number] = self.value.value[char_number]

        ints: list[int] = list()
        for item in self.info.midi_parsing.bytes_as_str:
            try:
                ints.append(int(item, 16))
            except ValueError:
                ints.append(ord(chars[int(item[1])]))

        return bytes(ints)
