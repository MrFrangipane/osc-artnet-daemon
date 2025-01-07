from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from oscartnetdaemon.core.configuration import Configuration


@dataclass_json
@dataclass
class Project:
    name: str
    configuration: Configuration
    fixtures: list[list[str]] = field(default_factory=list)
    patterns: dict[str, list[list[list[dict[str, int]]]]] = field(default_factory=dict)
