from dataclasses import dataclass


@dataclass
class ChannelInfo:
    first: int
    last: int
    count: int
