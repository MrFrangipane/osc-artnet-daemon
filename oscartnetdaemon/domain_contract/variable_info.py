from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class VariableInfo:
    name: str
    type: VariableType
