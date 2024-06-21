from mido import Message

from oscartnetdaemon.entities.midi.configuration import MIDIConfiguration
from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo
from oscartnetdaemon.entities.midi.control_update_info import MIDIControlUpdateInfo
from oscartnetdaemon.entities.midi.message_type_enum import MIDIMessageType
from oscartnetdaemon.entities.midi.parsing_info import MIDIParsingInfo


def midi_to_control_update(control: MIDIControlInfo, message: Message, parsing_info: MIDIParsingInfo) -> MIDIControlUpdateInfo | None:
    message_type = MIDIMessageType(message.type)
    if message_type != parsing_info.type:
        return

    if message_type == MIDIMessageType.PitchWheel and message.channel == parsing_info.channel:
        return MIDIControlUpdateInfo(
            control_name=control.name,
            value=float(message.pitch + 8192) / 16380.0
        )

    elif message_type == MIDIMessageType.NoteOn and message.channel == parsing_info.channel and message.note == parsing_info.note:
        return MIDIControlUpdateInfo(
            control_name=control.name,
            value=float(message.velocity) / 127.0
        )


def control_update_to_midi(control_update: MIDIControlUpdateInfo, configuration: MIDIConfiguration) -> Message:
    control = configuration.controls[control_update.control_name]
    if control.midi.type == MIDIMessageType.PitchWheel:
        return Message(
            type=MIDIMessageType.PitchWheel.value,
            channel=control.midi.channel,
            pitch=int(control_update.value * 16380.0 - 8192)
        )

    if control.midi.type == MIDIMessageType.NoteOn:
        return Message(
            type=MIDIMessageType.NoteOn.value,
            channel=control.midi.channel,
            note=control.midi.note,
            velocity=int(control_update.value * 127)
        )
