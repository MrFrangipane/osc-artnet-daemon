from dataclasses import dataclass


@dataclass
class DMXChannel:
    name: str = ""
    unused: bool = False
    value: float = 0.0
    value_default: float = 0.0
    channel_number: int = -1
