from dataclasses import dataclass, field

from oscartnetdaemon.core.osc.mood import Mood


@dataclass
class MoodStoreItem:
    before_punch: Mood = field(default_factory=Mood)
    a: Mood = field(default_factory=Mood)
    b: Mood = field(default_factory=Mood)
    c: Mood = field(default_factory=Mood)
    d: Mood = field(default_factory=Mood)
