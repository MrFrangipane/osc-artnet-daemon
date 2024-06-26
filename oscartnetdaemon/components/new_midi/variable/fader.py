from oscartnetdaemon.components.new_midi.io.message import MIDIMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.components.new_midi.io.message_type_enum import MIDIMessageType


class MIDIFader(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: MIDIVariableInfo = self.info
        self.value = notification.value
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
        info: MIDIVariableInfo = self.info
        channel_ok = info.midi_parsing.channel == message.channel
        device_ok = info.device_name == message.device_name
        # layer_ok = self.info.layer_name == "" or self.info.layer_name == context.current_layer.name
        # page_ok = self.info.page == -1 or self.info.page == context.current_page
        type_ok = message.type == info.midi_parsing.type

        if not device_ok or not type_ok or not channel_ok:
            return

        compliant = {
            MIDIMessageType.NoteOn: message.note == info.midi_parsing.note,
            MIDIMessageType.PitchWheel: True
        }

        if not compliant:
            return

        self.value.value = float(message.pitch + 8192) / 16380.0
        self.notification_queue_out.put(ChangeNotification(
            info=self.info,
            value=self.value
        ))
