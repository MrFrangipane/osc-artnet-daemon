from abc import ABC, abstractmethod

from oscartnetdaemon.components.midi.device import MIDIDevice
from oscartnetdaemon.components.midi.entities.control_update_info import MIDIControlUpdateInfo


class AbstractMIDIService(ABC):

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
