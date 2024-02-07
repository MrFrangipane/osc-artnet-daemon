from dataclasses import dataclass

from oscartnetdaemon.core.mood import Mood


@dataclass
class MoodStoreItem:
    before_punch: Mood = Mood()
    a: Mood = Mood()
    b: Mood = Mood()
    c: Mood = Mood()
    d: Mood = Mood()
