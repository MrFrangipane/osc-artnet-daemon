from dataclasses import fields

from oscartnetdaemon.core.fixture.base import BaseFixture
from oscartnetdaemon.core.fixture.group import FixtureGroup
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.show.channel_info import ShowItemChannelInfo
from oscartnetdaemon.core.show.group_info import ShowItemGroupInfo
from oscartnetdaemon.core.show.item import ShowItem
from oscartnetdaemon.core.show.show import Show


class ShowLoader:
    def __init__(self):
        self._default_mood = Mood()

        self._channel_start_index = 0
        self._group_index = 1
        self._group_size = 1
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
                show_items.append(self._fixture_to_show_item(fixture, is_group=False, group_position=0.5, group_place=1))
            else:
                self._group_size = len(fixture.fixtures)
                for i, sub_fixture in enumerate(fixture.fixtures):
                    show_items.append(self._fixture_to_show_item(
                        sub_fixture,
                        is_group=True,
                        group_position=float(i) / (len(fixture.fixtures) - 1),
                        group_place=i
                    ))
                self._group_index += 1

        return show_items

    def _fixture_to_show_item(self, fixture: BaseFixture, is_group, group_position, group_place) -> ShowItem:
        channel_count = len(fields(fixture.Mapping))

        group_info = ShowItemGroupInfo(
            index=self._group_index if is_group else 0,
            size=self._group_size if is_group else 1,
            position=group_position,
            place=group_place
        )

        channel_info = ShowItemChannelInfo(
            first=self._channel_start_index,
            last=self._channel_start_index + channel_count,
            count=channel_count
        )

        new_item = ShowItem(
            name=type(fixture).__name__,
            fixture=fixture,
            fixture_index=self._fixture_index,
            group_info=group_info,
            channel_info=channel_info
        )

        self._channel_start_index += new_item.channel_info.count
        self._fixture_index += 1

        return new_item
