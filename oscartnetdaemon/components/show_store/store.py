from oscartnetfixtures import OSCArtnetFixturesAPI

from oscartnetdaemon.components.show_store.abstract import AbstractShowStore
from oscartnetdaemon.components.show_store.loader import ShowLoader

from oscartnetdaemon.core.fixture.group import FixtureGroup


class ShowStore(AbstractShowStore):
    """
    Loads and stores all ShowItems (Fixtures) in a Show object
    """
    def __init__(self):
        super().__init__()

    def load_show(self):
        OSCArtnetFixturesAPI.reload_definitions()
        self.show = ShowLoader().from_fixtures(title="Show", fixtures=[
            FixtureGroup([OSCArtnetFixturesAPI.get_fixture("OctostripBar")() for _ in range(8)]),
            FixtureGroup([OSCArtnetFixturesAPI.get_fixture("Tristan200")() for _ in range(2)]),
            FixtureGroup([OSCArtnetFixturesAPI.get_fixture("TwoBrightPar")() for _ in range(5)]),
            FixtureGroup([OSCArtnetFixturesAPI.get_fixture("HeroWash")() for _ in range(2)]),
        ])

    def items_by_type(self, type_name):
        for item in self.show.items:
            if type(item.fixture).__name__ == type_name:
                yield item
