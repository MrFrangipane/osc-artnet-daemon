from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCRecallGroupInfo:
    name: str
    controls_osc_addresses: list[str]
