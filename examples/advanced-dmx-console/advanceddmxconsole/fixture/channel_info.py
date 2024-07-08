from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class ChannelInfo:
    name: str
    default_int: int = 0
    unused: bool = False
    master_dimmed: bool = False
