from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from advanceddmxconsole.fixture.fixture_type_info import FixtureTypeInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class FixtureInfo:
    name: str
    type: FixtureTypeInfo
