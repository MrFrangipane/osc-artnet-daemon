from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.domain_contract.variable_info import VariableInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class QuSbVariableInfo(VariableInfo):
    caption: str
    channel: int

