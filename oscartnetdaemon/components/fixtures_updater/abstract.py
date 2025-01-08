from abc import ABC, abstractmethod

from oscartnetdaemon.core.channel_info import ChannelInfo
from oscartnetdaemon.core.show.item_info import ShowItemInfo


class AbstractFixturesUpdater(ABC):
    def __init__(self):
        self.universe = bytearray(512)

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

    @staticmethod
    def set_pattern_edition_step(show_item_info: ShowItemInfo, step: dict[str, int]):
        pass
