from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.domain_contract.variable_info import VariableInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class ArtnetVariableInfo(VariableInfo):
    caption: str = ""
    index: int = -1
    scribble_caption: str = ""
    scribble_value: str = ""
    redirect: str = ""
    is_master: bool = False
