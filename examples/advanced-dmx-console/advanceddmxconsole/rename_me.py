from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from oscartnetdaemon.domain_contract.value.float import ValueFloat
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass

from advanceddmxconsole.fixture.base_definition import BaseFixtureDefinition
from advanceddmxconsole.artnet.io.artnet_server import ArtnetServer
from advanceddmxconsole.artnet.variable_info import ArtnetVariableInfo
from advanceddmxconsole.fixture.fixture_repository import FixtureRepository


class RenameMe(metaclass=SingletonMetaclass):
    def __init__(self):
        self.components: ServiceComponents | None = None
        self.fixture_repository = FixtureRepository()
        self.current_fixture: BaseFixtureDefinition | None = None
        self.fixture_list_buttons: list[AbstractVariable] = list()
        self.dmx_faders: list[AbstractVariable] = list()

        self.universe = bytearray(512)

    def initialize(self, server: ArtnetServer, components: ServiceComponents):
        self.server = server
        self.components = components
        self.fixture_repository.initialize(self.components)

        self.initialize_fixture_list_buttons()
        self.initialize_dmx_faders()

        self.display_fixture_list()
        # self.display_fixture(self.fixture_repository.fixtures[0])

    #
    # Handlers
    def handle_button(self, info: ArtnetVariableInfo):
        if info.name.startswith('Fixture.Button.Select') and info.index < self.fixture_repository.count():
            self.select_fixture(self.fixture_repository.fixtures[info.index])

    def handle_fader(self, info: ArtnetVariableInfo, value: ValueFloat):
        if self.current_fixture is None:
            return

        if info.index > len(self.current_fixture.channels) - 1:
            return

        channel = self.current_fixture.channels[info.index]
        channel.value = value.value

        universe_channel = self.current_fixture.universe_address + info.index
        self.universe[universe_channel] = int(value.value * 255)
        self.server.set_universe(self.universe)

    #
    # Mode Fixture list
    def initialize_fixture_list_buttons(self):
        self.fixture_list_buttons = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('Fixture.')
        ])

    def reset_fixture_list_captions(self):
        for variable_button in self.fixture_list_buttons:
            variable_button.info.caption = ""

    def display_fixture_list(self):
        self.reset_fixture_list_captions()
        for variable_index, fixture in enumerate(self.fixture_repository.fixtures):
            variable_button = self.fixture_list_buttons[variable_index]
            variable_button.info.caption = fixture.name

        self.notify_all(self.fixture_list_buttons)

    #
    # Mode DMX
    def initialize_dmx_faders(self):
        self.dmx_faders = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('DMX.')
        ])

    def reset_dmx_faders(self):
        for variable_fader in self.dmx_faders:
            variable_fader.info.caption = ""
            variable_fader.value.value = float(0.0)

    def select_fixture(self, fixture: BaseFixtureDefinition):
        self.current_fixture = fixture
        self.reset_dmx_faders()

        for fader_index, channel in enumerate(fixture.channels):
            variable_fader = self.dmx_faders[fader_index]
            variable_fader.info.caption = channel.function
            variable_fader.value.value = channel.value

        self.notify_all(self.dmx_faders)

    #
    # Notify
    def notify_all(self, variables):
        for variable in variables:
            self.notify(
                variable_name=variable.info.name,
                value=variable.value
            )

    def notify(self, variable_name: str, value: ValueFloat | None = None, update_value=True):
        self.components.notification_queue_out.put(ChangeNotification(
            variable_name=variable_name,
            value=value,
            update_value=update_value
        ))
