

from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.midi.midi_device import MIDIDevice
from oscartnetdaemon.components.midi.abstract_service import AbstractMidiService


class MidiService(AbstractMidiService):

    def __init__(self):
        super().__init__()

    def start(self):
        self.devices = dict()

        for device_info in Components().midi_configuration.devices.values():
            self.devices[device_info.name] = MIDIDevice(device_info)
            self.devices[device_info.name].components_singleton = Components
            self.devices[device_info.name].start()

    def stop(self):
        for device in self.devices.values():
            device.stop()
