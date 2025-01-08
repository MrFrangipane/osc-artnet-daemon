import logging

from oscartnetfixtures import OSCArtnetFixturesAPI

from oscartnetdaemon.components.show_store.abstract import AbstractShowStore
from oscartnetdaemon.components.show_store.loader import ShowLoader
from oscartnetdaemon.core.show.item import ShowItem
from oscartnetdaemon.core.show.item_info import ShowItemInfo

from oscartnetdaemon.core.fixture.group import FixtureGroup


_logger = logging.getLogger(__name__)


class ShowStore(AbstractShowStore):
    """
    Loads and stores all ShowItems (Fixtures) in a Show object
    """
    def __init__(self):
        super().__init__()

    def load_show(self, fixtures_structure: list[list[str]]) -> None:
        self._fixtures_structure = fixtures_structure
        self.reload_fixtures()

    def reload_fixtures(self) -> None:
        OSCArtnetFixturesAPI.reload_definitions()
        fixtures = [
            FixtureGroup([
                OSCArtnetFixturesAPI.get_fixture(fixture_type)() for fixture_type in fixture_group
            ]) for fixture_group in self._fixtures_structure
        ]

        self.show = ShowLoader().from_fixtures(title="Show", fixtures=fixtures)
        _logger.info(f"Loaded show fixtures")

    def items_by_type(self, type_name):  # FIXME make a dict ?
        for item in self.show.items:
            if type(item.fixture).__name__ == type_name:
                yield item

    def item_by_info(self, show_item_info: ShowItemInfo) -> ShowItem:
        for item in self.show.items:
            if item.info == show_item_info:
                return item
