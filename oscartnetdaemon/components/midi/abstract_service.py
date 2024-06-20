from abc import ABC, abstractmethod

from oscartnetdaemon.components.midi.midi_device import MIDIDevice


class AbstractMidiService(ABC):

    def __init__(self):
        self.devices: dict[str, MIDIDevice] = dict()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
