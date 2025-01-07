from dataclasses import dataclass

from dataclasses_json import dataclass_json

from oscartnetdaemon.core.configuration import Configuration


@dataclass_json
@dataclass
class Project:
    name: str
    configuration: Configuration
    fixtures: list[str]
