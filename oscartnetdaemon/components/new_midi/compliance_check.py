from oscartnetdaemon.components.new_midi.context import MIDIContext
from oscartnetdaemon.components.new_midi.io.message import MIDIMessage
from oscartnetdaemon.components.new_midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo


def check_notification(info: MIDIVariableInfo) -> bool:
    page_ok = (
        info.pagination_name == "" or
        info.page_number == -1 or
        info.page_number == MIDIContext().pagination_infos[info.pagination_name].current_page
    )

    return page_ok


def check_io_message(info: MIDIVariableInfo, message: MIDIMessage) -> bool:
    channel_ok = info.midi_parsing.channel == message.channel
    device_ok = info.device_name == message.device_name
    page_ok = (
        info.pagination_name == "" or
        info.page_number == -1 or
        info.page_number == MIDIContext().pagination_infos[info.pagination_name].current_page
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
