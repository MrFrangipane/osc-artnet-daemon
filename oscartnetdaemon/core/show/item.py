from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo
from oscartnetdaemon.core.show.channel_info import ShowItemChannelInfo


@dataclass
class ShowItem:
    name: str
    fixture: BaseFixture
    fixture_index: int
    group_info: ShowItemGroupInfo
    channel_info: ShowItemChannelInfo
