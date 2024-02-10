from oscartnetdaemon.components.show_store.abstract import AbstractShowStore
from oscartnetdaemon.components.show_store.loader import ShowLoader

from oscartnetdaemon.components.fixtures.octostrip_bar import OctostripBar
from oscartnetdaemon.components.fixtures.tristan_200 import Tristan200
from oscartnetdaemon.components.fixtures.two_bright_par import TwoBrightPar
from oscartnetdaemon.core.fixture.group import FixtureGroup


class ShowStore(AbstractShowStore):
    """
    Loads and stores all ShowItems (Fixtures) in a Show object
    """
    def __init__(self):
        super().__init__()

    def load_show(self):
        self.show = ShowLoader().from_fixtures(title="Show", fixtures=[
            FixtureGroup([OctostripBar() for _ in range(8)]),
            FixtureGroup([Tristan200() for _ in range(2)]),
            FixtureGroup([TwoBrightPar() for _ in range(5)]),
        ])

    def items_by_type(self, type_name):
        for item in self.show.items:
            if type(item.fixture).__name__ == type_name:
                yield item
