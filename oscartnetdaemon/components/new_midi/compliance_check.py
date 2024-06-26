from oscartnetdaemon.components.new_midi.context import MIDIContext
from oscartnetdaemon.components.new_midi.io.message import MIDIMessage
from oscartnetdaemon.components.new_midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo


def check_notification(info: MIDIVariableInfo) -> bool:
    return info.page_number == -1 or info.page_number == MIDIContext().current_pages[info.pagination_name]


def check_io_message(info: MIDIVariableInfo, message: MIDIMessage) -> bool:
    channel_ok = info.midi_parsing.channel == message.channel
    device_ok = info.device_name == message.device_name
    # layer_ok = self.info.layer_name == "" or self.info.layer_name == context.current_layer.name
    page_ok = (
        info.pagination_name == "" or
        info.page_number == -1 or
        info.page_number == MIDIContext().current_pages[info.pagination_name]
    )
    type_ok = message.type == info.midi_parsing.type

    if not device_ok or not type_ok or not channel_ok or not page_ok:
        return False

    compliant = {
        MIDIMessageType.NoteOn: message.note == info.midi_parsing.note,
        MIDIMessageType.PitchWheel: True
    }[message.type]

    if not compliant:
        return False

    return True
