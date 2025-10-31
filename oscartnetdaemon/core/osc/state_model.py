from dataclasses import dataclass, field
from enum import IntEnum

from oscartnetdaemon.core.osc.groups import Groups
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.osc.two_bright_par import TwoBrightPar
from oscartnetdaemon.core.osc.tristan_200 import Tristan200
from oscartnetdaemon.core.osc.pattern_edition import PatternEdition


@dataclass
class OSCStateModel:

    class Page(IntEnum):
        Mood = 0
        Groups = 1
        PatternEdition = 2
        Tristan200 = -1
        TwoBrightPar = -1

    autoplay_current_scene: int = -1
    autoplay_lastest_client: str = ""
    current_page: Page = Page.Mood
    groups: Groups = field(default_factory=Groups)
    mood: Mood = field(default_factory=Mood)
    pattern_edition: PatternEdition = field(default_factory=PatternEdition)
    tristan_200: Tristan200 = field(default_factory=Tristan200)
    two_bright_par: TwoBrightPar = field(default_factory=TwoBrightPar)
