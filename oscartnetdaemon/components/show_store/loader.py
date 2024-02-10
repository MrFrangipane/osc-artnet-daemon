from oscartnetdaemon.core.osc.mood import Mood
from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.fixture.group import FixtureGroup
from oscartnetdaemon.core.show.show import Show
from oscartnetdaemon.core.show.item import ShowItem


class ShowLoader:
    def __init__(self):
        self._default_mood = Mood()

        self._channel_start_index = 0
        self._group_index = 1
        self._fixture_index = 0

    def from_fixtures(self, title: str, fixtures: list[BaseFixture]) -> Show:
        return Show(
            title="Show",
            items=self._fixtures_to_show_items(fixtures)
        )

    def _fixtures_to_show_items(self, fixtures: list[BaseFixture]) -> list[ShowItem]:
        show_items = list()
        self._channel_start_index = 0
        self._group_index = 1
        self._fixture_index = 0

        for fixture in fixtures:
            if not isinstance(fixture, FixtureGroup):
                show_items.append(self._fixture_to_show_item(fixture, is_group=False))
            else:
                for sub_fixture in fixture.fixtures:
                    show_items.append(self._fixture_to_show_item(sub_fixture, is_group=True))
                self._group_index += 1

        return show_items

    def _fixture_to_show_item(self, fixture: BaseFixture, is_group) -> ShowItem:
        channel_count = len(fixture.map_to_channels(mood=self._default_mood, group_position=0.0))
        new_item = ShowItem(
            name=type(fixture).__name__,
            fixture=fixture,
            fixture_index=self._fixture_index,
            channel_first=self._channel_start_index,
            channel_last=self._channel_start_index + channel_count,
            channel_count=channel_count,
            group_index=self._group_index if is_group else 0
        )

        self._channel_start_index += new_item.channel_count
        self._fixture_index += 1

        return new_item
