from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from advanceddmxconsole.fixture.definition.varytec_hero_wash_300_fc import VarytecHeroWash300FC
from advanceddmxconsole.fixture.base_definition import BaseFixtureDefinition


class FixtureRepository:

    def __init__(self):
        self.components: ServiceComponents | None = None

        self.fixtures: list[BaseFixtureDefinition] = list()

    def initialize(self, components: ServiceComponents):
        self.components = components

        self.fixtures = [
            VarytecHeroWash300FC(name='Wash C'),
            VarytecHeroWash300FC(name='Wash J')
        ]

        universe_address = 0
        for fixture in self.fixtures:
            fixture.create_channels(universe_address)
            universe_address += len(fixture.Channels)

    def count(self):
        return len(self.fixtures)
