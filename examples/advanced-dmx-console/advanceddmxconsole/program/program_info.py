from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from advanceddmxconsole.fixture.fixture import Fixture


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class ProgramInfo:
    name: str
    fixtures: list[Fixture]
