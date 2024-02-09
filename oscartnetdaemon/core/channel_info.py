from dataclasses import dataclass


@dataclass
class ChannelInfo:
    dmx_index: int = 0
    fixture_index: int = 0
    group_index: int = 0
    value: int = 0
