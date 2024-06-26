from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.domain_contract.variable_info import VariableInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCVariableInfo(VariableInfo):
    caption: str
    osc_address: str
