from dataclasses import dataclass

from oscartnetdaemon.core.fixture.base import BaseFixture


@dataclass
class ShowItem:
    """
    This class represents a show item.

    :ivar name: The name of the show item.
    :vartype name: str

    :ivar fixture: The fixture associated with.
    :vartype fixture: BaseFixture

    :ivar fixture_index: The index of the fixture in the show.
    :vartype fixture_index: int

    :ivar group_index: The index of the group that the fixture belongs to.
    :vartype group_index: int

    :ivar channel_first: The first DMX channel of the fixture.
    :vartype channel_start: int

    :ivar channel_last: The last DMX channel of the fixture.
    :vartype channel_end: int

    :ivar channel_count: The number of channels of the fixture.
    :vartype channel_count: int
    """
    name: str

    fixture: BaseFixture
    fixture_index: int

    group_index: int  # which group
    group_position: float  # where in the group

    channel_first: int
    channel_last: int
    channel_count: int
