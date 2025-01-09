from dataclasses import dataclass, field

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PatternStepContainer:
    step: dict[int, dict[str, int]] = field(default_factory=dict)


@dataclass_json
@dataclass
class PatternGroupPlaceContainer:
    group_place: dict[int, PatternStepContainer] = field(default_factory=dict)


@dataclass_json
@dataclass
class PatternIndexContainer:
    pattern_index: dict[int, PatternGroupPlaceContainer] = field(default_factory=dict)


@dataclass_json
@dataclass
class PatternStoreContainer:
    fixture_type: dict[str, PatternIndexContainer] = field(default_factory=dict)
    pattern_names: list[str] = field(default_factory=lambda: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"])
