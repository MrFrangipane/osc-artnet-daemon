from oscartnetdaemon.components.new_midi.io.message import MIDIMessage
from oscartnetdaemon.components.new_midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from oscartnetdaemon.components.new_midi.compliance_check import check_io_message, check_notification
from oscartnetdaemon.components.new_midi.context import MIDIContext
from oscartnetdaemon.components.new_midi.page_direction_enum import MIDIPageDirection


class MIDIButton(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: MIDIVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.is_page_button and self.value.value == 1:
            if info.page_direction == MIDIPageDirection.Up:
                MIDIContext().pagination_infos[info.pagination_name].up()
            else:
                MIDIContext().pagination_infos[info.pagination_name].down()

            print(MIDIContext().pagination_infos[info.pagination_name].current_page)

        elif check_notification(info):
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
        if not check_io_message(self.info, message):
            return

        self.value.value = float(message.velocity / 127.0)
        self.notify_change()
