from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class AbstractIOMessage:
    """
    Inherit for each IO implementation, to store relevant IO data
    """
    pass
