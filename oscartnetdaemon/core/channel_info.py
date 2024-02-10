from dataclasses import dataclass


@dataclass
class ChannelInfo:
    """
    This class represents channel information.

    :ivar dmx_index: The DMX index of the ChannelInfo. Default is 0.
    :vartype dmx_index: int

    :ivar fixture_index: The fixture index of the ChannelInfo. Default is 0.
    :vartype fixture_index: int

    :ivar group_index: The group index of the ChannelInfo. Default is 0.
    :vartype group_index: int

    :ivar value: The value of the ChannelInfo. Default is 0.
    :vartype value: int
    """
    dmx_index: int = 0
    fixture_index: int = 0
    group_index: int = 0
    value: int = 0
