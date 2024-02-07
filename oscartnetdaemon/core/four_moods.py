from dataclasses import dataclass

from oscartnetdaemon.core.mood import Mood


# FIXME find better names for FourMoods and MoodStore
@dataclass
class FourMoods:
    before_punch: Mood = Mood()
    a: Mood = Mood()
    b: Mood = Mood()
    c: Mood = Mood()
    d: Mood = Mood()
