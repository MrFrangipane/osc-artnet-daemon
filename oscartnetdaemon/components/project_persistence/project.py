from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from oscartnetdaemon.core.configuration import Configuration
from oscartnetdaemon.core.pattern.store_containers import PatternStoreContainer


@dataclass_json
@dataclass
class Project:
    name: str
    configuration: Configuration
    fixtures: list[list[str]] = field(default_factory=list)
    patterns: PatternStoreContainer = field(default_factory=PatternStoreContainer)
