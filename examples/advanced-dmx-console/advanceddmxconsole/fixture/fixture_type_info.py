from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from advanceddmxconsole.fixture.channel_info import ChannelInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class FixtureTypeInfo:
    name: str
    channel_infos: list[ChannelInfo]
