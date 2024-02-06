from abc import ABC, abstractmethod

from oscartnetdaemon.core.mood import Mood


class BaseFixture(ABC):

    def __init__(self, address):
        self.address = address
        self.channels: bytearray

    @abstractmethod
    def update(self, mood: Mood):
        pass
