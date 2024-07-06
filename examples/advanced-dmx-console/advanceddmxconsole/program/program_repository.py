import copy
import json
import logging
import os

from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from advanceddmxconsole.fixture.fixture_repository import FixtureRepository
from advanceddmxconsole.program.program_info import ProgramInfo


_logger = logging.getLogger(__name__)


class ProgramRepository:
    DIR_PROGRAMS = 'programs'

    def __init__(self, universe: bytearray, fixture_repository: FixtureRepository):
        self.universe = universe
        self.components: ServiceComponents | None = None
        self.fixture_repository: FixtureRepository = fixture_repository
        self.programs: list[ProgramInfo] = list()
        self.copy_slot: ProgramInfo | None = None

    def initialize(self, components: ServiceComponents):
        if not self.fixture_repository.fixtures:
            _logger.warning(f"No fixture, has FixtureRepository been initialized ?")

        self.components = components
        self.load_programs()

    def load_programs(self):
        self.programs = list()

        files = os.listdir(self.DIR_PROGRAMS)
        for index in range(64):
            filename = f"{index}.json"

            if filename not in files:
                self.programs.append(ProgramInfo(
                    name=f"Prog.{index+1:02}",
                    index=index,
                    fixtures_snapshots=[fixture.snapshot() for fixture in self.fixture_repository.fixtures]
                ))

            else:
                filepath = os.path.abspath(os.path.join(self.DIR_PROGRAMS, filename))
                with open(filepath, 'r') as program_file:

                    data = json.load(program_file)
                    new_program: ProgramInfo = ProgramInfo.from_dict(data)

                    if not self.check_compliance(new_program):
                        _logger.warning(f"Not loaded")

                    else:
                        self.programs.append(new_program)
                        _logger.info(f"Loaded program '{new_program.name}' from file {filepath}")

    def count(self):
        return len(self.programs)

    def save(self, index: int):
        program = self.programs[index]
        program.fixtures_snapshots = list()
        for fixture in self.fixture_repository.fixtures:
            program.fixtures_snapshots.append(fixture.snapshot())

        filepath = os.path.abspath(os.path.join(self.DIR_PROGRAMS, f"{program.index}.json"))
        with open(filepath, 'w+') as program_file:
            json.dump(program.to_dict(), program_file, indent=2)

        _logger.info(f"Program '{program.name}' saved to {filepath}")

    def load(self, index: int) -> ProgramInfo | None:
        program = self.programs[index]

        if not self.check_compliance(program):
            return

        for fixture, fixture_snapshot in zip(self.fixture_repository.fixtures, program.fixtures_snapshots):
            for channel_index, value in enumerate(fixture_snapshot.channel_values):
                fixture.channels[channel_index].value = value
                self.universe[fixture.universe_address + channel_index] = int(value * 255)

        _logger.info(f"Program '{program.name}' loaded")
        return program

    def check_compliance(self, program: ProgramInfo):
        if len(self.fixture_repository.fixtures) != len(program.fixtures_snapshots):
            _logger.warning(f"Program '{program.name}' not compatible with current fixtures")
            return False

        for fixture, fixture_snapshot in zip(self.fixture_repository.fixtures, program.fixtures_snapshots):
            if fixture.info != fixture_snapshot.info:
                _logger.warning(f"Program '{program.name}' not compatible with current fixtures")
                return False

        return True

    def reset(self, index: int):
        program = self.programs[index]

        for fixture, fixture_snapshot in zip(self.fixture_repository.fixtures, program.fixtures_snapshots):
            for channel_index, channel in enumerate(fixture.channels):
                channel.value = channel.value_default
                fixture_snapshot.channel_values[channel_index] = channel.value_default
                self.universe[fixture.universe_address + channel_index] = int(channel.value * 255)

    def copy(self, index: int):
        self.copy_slot = copy.deepcopy(self.programs[index])

    def paste(self, index: int):
        self.programs[index] = copy.deepcopy(self.copy_slot)
        self.load(index)
