from dataclasses import dataclass

# FIXME: Separate concepts of definition and actual value


@dataclass
class BaseDMXChannel:
    function: str = ""
    unused: bool = False
    value: int = 0
    value_default: int = 0
    channel_number: int = -1


@dataclass
class DMXChannel(BaseDMXChannel):
    pass


@dataclass
class DMXChannelFloat(BaseDMXChannel):
    value: float = 0
    value_default: float = 0
