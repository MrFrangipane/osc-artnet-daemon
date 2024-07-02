from dataclasses import dataclass

# FIXME: Separate concepts of definition and actual value


@dataclass
class BaseDMXChannel:
    function: str = ""
    unused: bool = False
    value: float = 0.0
    value_default: float = 0.0
    channel_number: int = -1


@dataclass
class DMXChannel(BaseDMXChannel):
    pass


@dataclass
class DMXChannelFloat(BaseDMXChannel):
    pass
