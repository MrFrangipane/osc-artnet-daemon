from multiprocessing import Process, Queue

import mido

from oscartnetdaemon.entities.midi.device_info import MIDIDeviceInfo
from oscartnetdaemon.entities.midi.configuration import MIDIConfiguration


def receive(queue: Queue, port_name: str, configuration: MIDIConfiguration):
    midi_in = mido.open_input(port_name)
    while True:
        message = midi_in.receive()
        print(message)
        for control in configuration.controls.values():
            print(control.midi)
        queue.put(message)


def send(queue: Queue, port_name: str, configuration: MIDIConfiguration):
    midi_out = mido.open_output(port_name)
    while True:
        message = queue.get()
        midi_out.send(message)


class MIDIDevice:
    def __init__(self, info: MIDIDeviceInfo):
        self.info = info
        self.queue_in = Queue()
        self.queue_out = Queue()
        self.process_in: Process = None
        self.process_out: Process = None
        self.components_singleton = None  # FIXME: WTF is that ?!

    def start(self):
        configuration = self.components_singleton().midi_configuration
        self.process_in = Process(target=receive, args=(self.queue_in, self.info.in_port_name, configuration))
        self.process_out = Process(target=send, args=(self.queue_out, self.info.out_port_name, configuration))

        self.process_in.start()
        self.process_out.start()

    def stop(self):
        self.process_in.terminate()
        self.process_out.terminate()

    def send(self, message):
        self.queue_out.put(message)

    def receive(self):
        return self.queue_in.get()
