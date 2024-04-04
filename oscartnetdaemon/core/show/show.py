from dataclasses import dataclass, field

from oscartnetdaemon.core.show.item import ShowItem


@dataclass
class Show:
    """
    This class represents a show.

    :ivar title: The title of the show.
    :vartype title: str

    :ivar items: The items/scenes of the show. Default is an empty list.
    :vartype items: list[ShowItem]
    """
    title: str
    items: list[ShowItem] = field(default_factory=list)
    groups_dimmers: list[float] = field(default_factory=lambda: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
