from multiprocessing import Queue
from threading import Thread

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.midi.abstract_service import AbstractMidiService
from oscartnetdaemon.components.midi.message_parser import *  # TODO
from oscartnetdaemon.components.midi.midi_device import MIDIDevice


class MidiService(AbstractMidiService):

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.queue_in: Queue[Message] = Queue()
        self.queues_out: dict[str, Queue[Message]] = dict()
        self._thread: Thread = None

    def start(self):
        self.devices = dict()

        #
        # CONTROLS REPOSITORY HERE ?
        #

        for device_info in Components().midi_configuration.devices.values():
            self.devices[device_info.name] = MIDIDevice(device_info, self.queue_in)
            self.devices[device_info.name].components_singleton = Components
            self.devices[device_info.name].start()

        self.is_running = True
        self._thread = Thread(target=self.loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.is_running = False
        for device in self.devices.values():
            device.stop()

    def loop(self):
        while self.is_running:
            message = self.queue_in.get()
            #
            # CONTROLS AND DATA UPDATE HERE
            #
            print(">", message)
