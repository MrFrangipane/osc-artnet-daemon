from multiprocessing import Process, Queue

import mido

from oscartnetdaemon.entities.midi.configuration import MIDIConfiguration
from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.message import MIDIMessage


def receive(queue_in: Queue, queue_out: Queue, device_info: MIDIDeviceInfo, configuration: MIDIConfiguration):
    midi_in = mido.open_input(device_info.in_port_name)
    try:
        while True:
            mido_message = midi_in.receive()
            mido_message_vars = vars(mido_message)
            # print(mido_message_vars)
            mido_message_vars['device'] = device_info
            mido_message_vars['raw_message'] = mido_message  # This will disappear when dealing with midi out
            message = MIDIMessage.from_dict(mido_message_vars)
            queue_in.put(message)
            queue_out.put(message)

    except KeyboardInterrupt:
        midi_in.close()


def send(queue_out: Queue, device_info: MIDIDeviceInfo, configuration: MIDIConfiguration):
    midi_out = mido.open_output(device_info.out_port_name)
    try:
        while True:
            message = queue_out.get()
            midi_out.send(message.raw_message)
    except KeyboardInterrupt:
        midi_out.close()


class MIDIDevice:
    def __init__(self, info: MIDIDeviceInfo, queue_in: Queue):
        self.info = info
        self.queue_in: Queue[MIDIMessage] = queue_in
        self.queue_out: Queue[MIDIMessage] = Queue()
        self.process_in: Process = None
        self.process_out: Process = None
        self.components_singleton = None  # FIXME: WTF is that ?!

    def start(self):
        configuration = self.components_singleton().midi_configuration
        self.process_in = Process(target=receive, args=(self.queue_in, self.queue_out, self.info, configuration))
        self.process_out = Process(target=send, args=(self.queue_out, self.info, configuration))

        self.process_in.start()
        self.process_out.start()

    def stop(self):
        self.process_in.terminate()
        self.process_out.terminate()
