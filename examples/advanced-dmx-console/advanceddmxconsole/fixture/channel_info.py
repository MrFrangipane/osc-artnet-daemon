from dataclasses import dataclass


@dataclass
class ChannelInfo:
    name: str
    default_int: int = 0
    unused: bool = False
