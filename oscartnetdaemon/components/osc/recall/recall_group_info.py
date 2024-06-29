from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.osc.variable_info import OSCVariableInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCRecallGroupInfo:
    name: str
    target_variables: dict[str, OSCVariableInfo]
    recall_slots: dict[str, OSCVariableInfo]
