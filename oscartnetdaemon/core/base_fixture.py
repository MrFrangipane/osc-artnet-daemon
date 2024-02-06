from abc import ABC, abstractmethod

from oscartnetdaemon.core.mood import Mood


class BaseFixture(ABC):

    def __init__(self, address=0):
        self.address = address
        self._channels: bytearray = bytearray(0)

    @property
    def channels(self) -> bytearray:
        return self._channels

    @abstractmethod
    def update(self, mood: Mood, group_position: float = 0):
        pass
