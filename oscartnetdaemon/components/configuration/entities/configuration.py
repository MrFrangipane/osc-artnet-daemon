from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class ConfigurationInfo:
    root_folder: str
    midi_filenames: list[str]

