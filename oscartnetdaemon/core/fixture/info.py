from dataclasses import dataclass


@dataclass
class FixtureInfo:
    name: str = "<unknown fixture>"
    channel_start: int = 0
    channel_count: int = 0
    group_index: int = 0
