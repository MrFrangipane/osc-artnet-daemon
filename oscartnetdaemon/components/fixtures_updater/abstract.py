from abc import ABC, abstractmethod

from oscartnetdaemon.components.show_store.store import ShowStore
from oscartnetdaemon.core.channel_info import ChannelInfo


class AbstractFixturesUpdater(ABC):
    def __init__(self):
        self.universe = bytearray(512)
        self._show_store: ShowStore = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def channels_info(self) -> list[ChannelInfo]:
        """Returns a list of ChannelInfo. One for each active channel in the universe"""
        pass
