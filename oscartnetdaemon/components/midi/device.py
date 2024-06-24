from multiprocessing import Process, Queue

import mido

from oscartnetdaemon.components.midi.entities.configuration import MIDIConfiguration
from oscartnetdaemon.components.midi.entities.device_info import MIDIDeviceInfo
from oscartnetdaemon.components.midi.entities.message import MIDIMessage
from oscartnetdaemon.components.midi.entities.message_type_enum import MIDIMessageType


def receive(queue_in: "Queue[MIDIMessage]", device_info: MIDIDeviceInfo, configuration: MIDIConfiguration):
    midi_in = mido.open_input(device_info.in_port_name)
    try:
        while True:
            mido_message = midi_in.receive(block=False)  # don't block, we want the KeyboardInterrupt to work
            if mido_message is None:
                continue
            mido_message_vars = vars(mido_message)
            # print(mido_message_vars)
            mido_message_vars['device'] = device_info
            try:
                message = MIDIMessage.from_dict(mido_message_vars)
                queue_in.put(message)
            except ValueError:
                print(f'Midi device cant deal with <{mido_message}>')

    except KeyboardInterrupt:
        midi_in.close()


def send(queue_out: "Queue[MIDIMessage]", device_info: MIDIDeviceInfo, configuration: MIDIConfiguration):
    midi_out = mido.open_output(device_info.out_port_name)
    try:
        while True:
            message = queue_out.get()
            if message.type == MIDIMessageType.PitchWheel:
                midi_out.send(mido.Message(
                    type=message.type.value,
                    channel=message.channel,
                    pitch=message.pitch
                ))
            elif message.type == MIDIMessageType.NoteOn:
                midi_out.send(mido.Message(
                    type=message.type.value,
                    channel=message.channel,
                    note=message.note,
                    velocity=message.velocity
                ))
    except KeyboardInterrupt:
        midi_out.close()


class MIDIDevice:
    def __init__(self, info: MIDIDeviceInfo, queue_in: Queue, configuration: MIDIConfiguration):
        self.configuration = configuration
        self.info = info
        self.queue_in: Queue[MIDIMessage] = queue_in
        self.queue_out: Queue[MIDIMessage] = Queue()
        self.process_in: Process = None
        self.process_out: Process = None

    def start(self):
        self.process_in = Process(target=receive, args=(self.queue_in, self.info, self.configuration))
        self.process_out = Process(target=send, args=(self.queue_out, self.info, self.configuration))

        self.process_in.start()
        self.process_out.start()

    def stop(self):
        self.process_in.kill()
        self.process_out.kill()
