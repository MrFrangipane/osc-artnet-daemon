from oscartnetdaemon.components.new_midi.context import MIDIContext
from oscartnetdaemon.components.new_midi.io.message import MIDIMessage
from oscartnetdaemon.components.new_midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo


class MIDIComplianceChecker:
    @staticmethod
    def with_current_page(info: MIDIVariableInfo) -> bool:
        page_ok = (
            info.pagination_name == "" or
            info.page_number == -1 or
            info.page_number == MIDIContext().pagination_infos[info.pagination_name].current_page
        )

        return page_ok

    @staticmethod
    def with_current_layer(info: MIDIVariableInfo) -> bool:
        if info.is_layer_button:
            return True

        elif info.layer_group_name != "":
            return info.layer_name == MIDIContext().layer_group_infos[info.layer_group_name].current_layer_name

        return True

    @staticmethod
    def with_io_message(info: MIDIVariableInfo, message: MIDIMessage) -> bool:
        device_ok = info.device_name == message.device_name
        channel_ok = info.midi_parsing.channel == message.channel
        type_ok = message.type == info.midi_parsing.type
        layer_ok = MIDIComplianceChecker.with_current_layer(info)
        page_ok = (
            info.pagination_name == "" or
            info.page_number == -1 or
            info.page_number == MIDIContext().pagination_infos[info.pagination_name].current_page
        )

        if not device_ok or not layer_ok or not type_ok or not channel_ok or not page_ok:
            return False

        compliant = {
            MIDIMessageType.NoteOn: message.note == info.midi_parsing.note,
            MIDIMessageType.PitchWheel: True
        }[message.type]

        if not compliant:
            return False

        return True
