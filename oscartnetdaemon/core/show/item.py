from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.show.group_info import GroupInfo
from oscartnetdaemon.core.show.channel_info import ChannelInfo


@dataclass
class ShowItem:
    name: str
    fixture: BaseFixture
    fixture_index: int
    group: GroupInfo
    channel: ChannelInfo
