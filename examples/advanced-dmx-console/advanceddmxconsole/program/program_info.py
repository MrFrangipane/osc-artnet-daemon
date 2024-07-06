from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from advanceddmxconsole.program.fixture_snapshot import FixtureSnapshot


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class ProgramInfo:
    name: str
    index: int
    fixtures_snapshots: list[FixtureSnapshot]
