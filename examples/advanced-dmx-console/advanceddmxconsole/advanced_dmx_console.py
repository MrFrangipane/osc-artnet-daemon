import logging
import os.path
from copy import deepcopy

from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from oscartnetdaemon.domain_contract.value.float import ValueFloat
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass

from advanceddmxconsole.fixture.fixture import Fixture
from advanceddmxconsole.fixture.fixture_repository import FixtureRepository
from advanceddmxconsole.program.program_info import ProgramInfo
from advanceddmxconsole.program.program_repository import ProgramRepository
from advanceddmxconsole.variable_info import ArtnetVariableInfo
# from advanceddmxconsole.io.io import ArtnetIO  # FIXME circular import


_logger = logging.getLogger(__name__)


class AdvancedDmxConsole(metaclass=SingletonMetaclass):

    def __init__(self):
        self.universe = bytearray(512)

        self.components: ServiceComponents | None = None

        self.io: "ArtnetIO | None" = None

        self.fixture_repository = FixtureRepository()
        self.current_fixture: Fixture | None = None
        self.fixture_pager_index: int = 0  # Fixme move all selection logic to repository
        self.fixture_list_buttons: list[AbstractVariable] = list()
        self.fixture_copy_slot: Fixture | None = None

        self.program_repository = ProgramRepository(universe=self.universe, fixture_repository=self.fixture_repository)
        self.current_program: ProgramInfo | None = None
        self.program_list_select_buttons: list[AbstractVariable] = list()
        self.program_list_save_buttons: list[AbstractVariable] = list()

        self.dmx_faders: list[AbstractVariable] = list()

    def initialize(self, io: "ArtnetIO", components: ServiceComponents):
        self.io = io
        self.components = components

        if not os.path.isdir(ProgramRepository.DIR_PROGRAMS):
            os.mkdir(ProgramRepository.DIR_PROGRAMS)

        self.fixture_repository.initialize(self.components)
        self.fixture_pager_index = 0
        self.program_repository.initialize(self.components)

        self.initialize_fixture_list_buttons()
        self.initialize_dmx_faders()
        self.initialize_program_list_buttons()

        self.display_fixture_list()
        self.display_program_list()

        self.initialize_universe()

    #
    # Handlers
    def handle_button(self, info: ArtnetVariableInfo):
        # Fixture
        if info.name.startswith('Fixture.Button.Select') and info.index < self.fixture_repository.count():
            self.select_fixture(info.index)

        elif info.name == 'Channel.Up':
            self.select_next_fixture()

        elif info.name == 'Channel.Down':
            self.select_previous_fixture()

        elif info.name == 'DMX.Button.Reset':
            self.reset_fixture()

        elif info.name == 'DMX.Button.Copy':
            self.copy_fixture()

        elif info.name == 'DMX.Button.Paste':
            self.paste_fixture()

        # Program
        elif info.name.startswith('Program.Button.Select') and info.index < self.program_repository.count():
            self.select_program(info.index)

        elif info.name.startswith('Program.Button.Rec') and info.index < self.program_repository.count():
            self.save_program(info.index)

        elif info.name == 'Program.Button.Reset':
            self.reset_program()

        elif info.name == 'Program.Button.Copy':
            self.copy_program()

        elif info.name == 'Program.Button.Paste':
            self.paste_program()

    def handle_fader(self, info: ArtnetVariableInfo, value: ValueFloat):
        if self.current_fixture is None:
            return

        if info.index > len(self.current_fixture.channels) - 1:
            return

        channel = self.current_fixture.channels[info.index]
        channel.value = value.value

        universe_channel = self.current_fixture.universe_address + info.index
        self.universe[universe_channel] = int(value.value * 255)
        self.io.set_universe(self.universe)

    #
    # Mode Fixture list
    def initialize_fixture_list_buttons(self):
        self.fixture_list_buttons = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('Fixture.Button.Select')
        ])

    def reset_fixture_list_captions(self):
        for variable_button in self.fixture_list_buttons:
            variable_button.info.caption = ""

    def display_fixture_list(self):
        self.reset_fixture_list_captions()
        for variable_index, fixture in enumerate(self.fixture_repository.fixtures):
            variable_button = self.fixture_list_buttons[variable_index]
            variable_button.info.caption = fixture.info.name

        self.notify_all(self.fixture_list_buttons)

    #
    # Mode DMX
    def initialize_dmx_faders(self):
        self.dmx_faders = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('DMX.Fader')
        ])

    def reset_dmx_faders(self):
        for variable_fader in self.dmx_faders:
            variable_fader.info.caption = ""
            variable_fader.value.value = 0.0

    def select_fixture(self, index: int):
        self.components.shared_data.set_selected_fixture_index(index)
        self.current_fixture = self.fixture_repository.select(index)
        self.current_fixture_to_faders()

    def current_fixture_to_faders(self):
        self.fixture_pager_index = self.fixture_repository.fixtures.index(self.current_fixture)
        self.reset_dmx_faders()

        for fader_index, channel in enumerate(self.current_fixture.channels):
            variable_fader = self.dmx_faders[fader_index]
            variable_fader.info.caption = channel.name
            variable_fader.value.value = channel.value

        self.notify_all(self.dmx_faders)

    def select_next_fixture(self):
        self.fixture_pager_index = (self.fixture_pager_index + 1) % self.fixture_repository.count()
        self.select_fixture(self.fixture_pager_index)

    def select_previous_fixture(self):
        self.fixture_pager_index = (self.fixture_pager_index - 1) % self.fixture_repository.count()
        self.select_fixture(self.fixture_pager_index)

    def reset_fixture(self):
        for channel in self.current_fixture.channels:
            channel.value = channel.value_default

        self.current_fixture_to_faders()

    def copy_fixture(self):
        self.fixture_copy_slot = deepcopy(self.current_fixture)

    def paste_fixture(self):
        if self.fixture_copy_slot is None:
            return

        type_source = self.fixture_copy_slot.info.type
        type_target = self.current_fixture.info.type
        if type_source != type_target:
            _logger.info(f"Cannot paste '{type_source.name}' onto '{type_target.name}'")
            return

        for index, channel in enumerate(self.current_fixture.channels):
            channel.value = self.fixture_copy_slot.channels[index].value

        self.current_fixture_to_faders()

    #
    # Mode Program
    def initialize_program_list_buttons(self):
        self.program_list_select_buttons = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('Program.Button.Select')
        ])
        self.program_list_save_buttons = list([
            variable for name, variable in self.components.variable_repository.variables.items()
            if name.startswith('Program.Button.Rec')
        ])

    def reset_program_list_captions(self):
        for variable_button in self.program_list_select_buttons:
            variable_button.info.caption = ""

    def display_program_list(self):
        self.reset_program_list_captions()
        for variable_index, program in enumerate(self.program_repository.programs):
            variable_button = self.program_list_select_buttons[variable_index]
            variable_button.info.caption = program.name

        self.notify_all(self.program_list_select_buttons)

    def select_program(self, index: int):
        self.current_program = self.program_repository.load(index)
        self.select_fixture(self.fixture_pager_index)
        self.io.set_universe(self.universe)

        self.components.shared_data.set_current_program_name(self.current_program.name)
        self.components.shared_data.set_has_current_program_changed(True)

    def save_program(self, index: int):
        new_name = self.components.shared_data.get_current_program_name()
        self.program_repository.save(index, new_name)
        self.display_program_list()

    def reset_program(self):
        self.program_repository.reset(self.current_program.index)
        self.select_fixture(self.fixture_pager_index)
        self.io.set_universe(self.universe)

    def copy_program(self):
        self.program_repository.copy(self.current_program.index)

    def paste_program(self):
        self.program_repository.paste(self.current_program.index)
        self.select_fixture(self.fixture_pager_index)
        self.io.set_universe(self.universe)
        self.display_program_list()

    #
    # Universe
    def initialize_universe(self):
        for fixture in self.fixture_repository.fixtures:
            for channel in fixture.channels:
                universe_channel = fixture.universe_address + channel.channel_number
                self.universe[universe_channel] = int(channel.value * 255)

        self.io.set_universe(self.universe)

    #
    # Notify
    def notify_all(self, variables):
        for variable in variables:
            self.notify(
                variable_name=variable.info.name,
                value=variable.value
            )

    def notify(self, variable_name: str, value: ValueFloat | None = None):
        self.components.notification_queue_out.put(ChangeNotification(
            variable_name=variable_name,
            new_value=value
        ))
