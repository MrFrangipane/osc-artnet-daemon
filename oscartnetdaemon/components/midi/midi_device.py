from multiprocessing import Process, Queue

import mido

from oscartnetdaemon.entities.midi.configuration import MIDIConfiguration
from oscartnetdaemon.entities.midi.control_update_info import MIDIControlUpdateInfo
from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.message_type_enum import MIDIMessageType
from oscartnetdaemon.entities.midi.parsing_info import MIDIParsingInfo
from oscartnetdaemon.entities.midi.control_info import MIDIControlInfo


def midi_to_control_update(control: MIDIControlInfo, message: mido.Message, parsing_info: MIDIParsingInfo) -> MIDIControlUpdateInfo | None:
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


def control_update_to_midi(control_update: MIDIControlUpdateInfo, configuration: MIDIConfiguration) -> mido.Message:
    control = configuration.controls[control_update.control_name]
    if control.midi.type == MIDIMessageType.PitchWheel:
        return mido.Message(
            type=MIDIMessageType.PitchWheel.value,
            channel=control.midi.channel,
            pitch=int(control_update.value * 16380.0 - 8192)
        )


def receive(queue_in: Queue, queue_out: Queue, port_name: str, configuration: MIDIConfiguration):
    midi_in = mido.open_input(port_name)
    while True:
        message = midi_in.receive()
        print(">", message)

        for control in configuration.controls.values():
            control_update = midi_to_control_update(control, message, control.midi)
            if control_update is not None:
                if control.feedback_messages:
                    queue_out.put(control_update)
                queue_in.put(control_update)


def send(queue_out: Queue, port_name: str, configuration: MIDIConfiguration):
    midi_out = mido.open_output(port_name)
    while True:
        control_update = queue_out.get()
        message = control_update_to_midi(control_update, configuration)
        if message is not None:
            midi_out.send(message)


class MIDIDevice:
    def __init__(self, info: MIDIDeviceInfo):
        self.info = info
        self.queue_in: Queue[MIDIControlUpdateInfo] = Queue()
        self.queue_out: Queue[MIDIControlUpdateInfo] = Queue()
        self.process_in: Process = None
        self.process_out: Process = None
        self.components_singleton = None  # FIXME: WTF is that ?!

    def start(self):
        configuration = self.components_singleton().midi_configuration
        self.process_in = Process(target=receive, args=(self.queue_in, self.queue_out, self.info.in_port_name, configuration))
        self.process_out = Process(target=send, args=(self.queue_out, self.info.out_port_name, configuration))

        self.process_in.start()
        self.process_out.start()

    def stop(self):
        self.process_in.terminate()
        self.process_out.terminate()
