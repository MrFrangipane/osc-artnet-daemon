from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification

from advanceddmxconsole.fixture.definition.varytec_hero_wash_300_fc import VarytecHeroWash300FC
from advanceddmxconsole.fixture.base_definition import BaseFixtureDefinition


class FixtureRepository:

    def __init__(self, components: ServiceComponents):
        self.components = components

        self.fixtures: list[BaseFixtureDefinition] = list()

        self.fixture_list_variables: list[AbstractVariable] = list()
        self.dmx_variables: list[AbstractVariable] = list()

    def initialize(self):
        self.fixtures = [
            VarytecHeroWash300FC('Wash C'),
            VarytecHeroWash300FC('Wash J')
        ]

        start_channel = 1
        for fixture in self.fixtures:
            fixture.create_channels(start_channel)
            start_channel += len(fixture.Channels) + 2

        self.initialize_fixture_list_variables()
        self.initialize_dmx_variables()

        self.display_fixture_list()
        self.display_fixture(self.fixtures[0])

    #
    # Mode Fixture list
    def initialize_fixture_list_variables(self):
        self.fixture_list_variables = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('Fixture.')
        ])

    def reset_fixture_variables(self):
        for variable in self.fixture_list_variables:
            variable.info.caption = ""

    def display_fixture_list(self):
        self.reset_fixture_variables()
        for variable_index, fixture in enumerate(self.fixtures):
            variable = self.fixture_list_variables[variable_index]
            variable.info.caption = fixture.name

        self.notify_all(self.fixture_list_variables)

    #
    # Mode DMX
    def initialize_dmx_variables(self):
        self.dmx_variables = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('DMX.')
        ])

    def reset_dmx_variables(self):
        for variable in self.dmx_variables:
            variable.info.caption = ""
            variable.value.value = float(0.0)

    def display_fixture(self, fixture):
        self.reset_dmx_variables()
        for variable_index, channel in enumerate(fixture.channels):
            variable = self.dmx_variables[variable_index]
            variable.info.caption = channel.function
            variable.value.value = float(channel.value_default / 255.0)

        self.notify_all(self.dmx_variables)

    def notify_all(self, variables):
        for variable in variables:
            self.components.notification_queue_out.put(ChangeNotification(
                variable_name=variable.info.name,
                update_value=False
            ))
