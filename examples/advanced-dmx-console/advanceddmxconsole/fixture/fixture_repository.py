from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from advanceddmxconsole.fixture.fixture import Fixture


class FixtureRepository:

    def __init__(self):
        self.components: ServiceComponents | None = None

        self.fixtures: list[Fixture] = list()

    def initialize(self, components: ServiceComponents):
        self.components = components

        for fixture_info in self.components.configuration.fixtures.values():
            self.fixtures.append(Fixture(fixture_info))

        universe_address = 0
        for fixture in self.fixtures:
            fixture.create_channels(universe_address)
            universe_address += len(fixture.info.type.channels)

    def count(self):
        return len(self.fixtures)

    def fixture(self, index: int) -> Fixture:
        return self.fixtures[index % len(self.fixtures)]
