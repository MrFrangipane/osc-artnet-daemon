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


"""

    # fixme: move this to a "session manager" class
    def load_fixtures(self):
        self._fixtures = [
            FixtureGroup([OctostripBar() for _ in range(8)]),
            FixtureGroup([
                Tristan200(address=48),  # fixme: compute addresses once in "session manager"
                Tristan200(address=66)
            ]),
            FixtureGroup([TwoBrightPar() for _ in range(5)]),
        ]

    # fixme: move this to a "session manager" class
    def channels_info(self) -> list[ChannelInfo]:
        pass

    # fixme: move this to a "session manager" class
    def fixtures_info(self) -> list[FixtureInfo]:
        infos = list()
        dmx_index = 0
        group_index = 1
        fixture_index = 0
        for fixture in self._fixtures:
            if isinstance(fixture, FixtureGroup):
                for sub_fixture in fixture.fixtures:
                    infos.append(FixtureInfo(
                        name=f"{fixture_index:02d} {type(sub_fixture).__name__}",
                        channel_start=dmx_index,
                        channel_count=len(fields(sub_fixture.Mapping)),
                        group_index=group_index
                    ))
                    dmx_index += len(fields(sub_fixture.Mapping))
                    fixture_index += 1
                group_index += 1
            else:
                infos.append(FixtureInfo(
                    name=f"{fixture_index:02d} {type(fixture).__name__}",
                    channel_start=dmx_index,
                    channel_count=len(fields(fixture.Mapping)),
                    group_index=group_index
                ))
                dmx_index += len(fields(fixture.Mapping))
                fixture_index += 1
                group_index += 1

        return infos
"""
