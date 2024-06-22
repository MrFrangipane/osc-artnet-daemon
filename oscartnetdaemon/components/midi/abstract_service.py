from abc import ABC, abstractmethod

from oscartnetdaemon.components.midi.midi_device import MIDIDevice
from oscartnetdaemon.entities.midi.control_update_info import MIDIControlUpdateInfo


class AbstractMidiService(ABC):

    def __init__(self):
        self.devices: dict[str, MIDIDevice] = dict()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def notify_update(self, update_info: MIDIControlUpdateInfo):
        pass
