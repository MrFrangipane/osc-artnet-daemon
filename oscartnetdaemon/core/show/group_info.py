from dataclasses import dataclass


@dataclass
class GroupInfo:
    index: int  # which group
    position: float  # where in the group [0.0, 1.0]
    place: int  # where in the group [1, len()]
    size: int  # how many in the group in total
