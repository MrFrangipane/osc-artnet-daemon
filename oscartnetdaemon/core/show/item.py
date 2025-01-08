from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.show.item_info import ShowItemInfo


@dataclass
class ShowItem:
    fixture: BaseFixture
    info: ShowItemInfo
