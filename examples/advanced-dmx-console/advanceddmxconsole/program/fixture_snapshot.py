from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from advanceddmxconsole.fixture.fixture_info import FixtureInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class FixtureSnapshot:
    info: FixtureInfo
    channel_values: list[float]
