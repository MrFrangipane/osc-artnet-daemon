from dataclasses import dataclass


@dataclass
class ShowItemChannelInfo:
    first: int
    last: int
    count: int
