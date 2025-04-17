from abc import ABC, abstractmethod

from oscartnetdaemon.core.midi_tempo_info import MIDITempoInfo


class AbstractMIDITempo(ABC):

    @abstractmethod
    def is_injectable(self) -> bool:
        pass

    @abstractmethod
    def info(self) -> MIDITempoInfo:
        pass

    @abstractmethod
    def set_in_port(self, port_name):
        pass

    @abstractmethod
    def set_out_port(self, port_name):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def send_tap(self):
        pass
