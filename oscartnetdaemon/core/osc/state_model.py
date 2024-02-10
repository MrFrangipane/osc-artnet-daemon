from dataclasses import dataclass, field
from enum import IntEnum

from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.osc.tristan_200 import Tristan200


@dataclass
class OSCStateModel:

    class Page(IntEnum):
        Mood = 0
        Setting = 1
        Tristan200 = 2

    current_page: Page = Page.Mood
    mood: Mood = field(default_factory=Mood)
    tristan_200: Tristan200 = field(default_factory=Tristan200)

