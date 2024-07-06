import logging

from oscartnetdaemon.domain_contract.service_components import ServiceComponents

from advanceddmxconsole.fixture.fixture_repository import FixtureRepository
from advanceddmxconsole.program.program_info import ProgramInfo


_logger = logging.getLogger(__name__)


class ProgramRepository:

    def __init__(self, fixture_repository: FixtureRepository):
        self.components: ServiceComponents | None = None
        self.fixture_repository: FixtureRepository = fixture_repository
        self.programs = [
            ProgramInfo("Prog 1", list()),
            ProgramInfo("Prog 2", list()),
            ProgramInfo("Prog 3", list())
        ]

    def initialize(self, components: ServiceComponents):
        if not self.fixture_repository.fixtures:
            _logger.warning(f"No fixture, has FixtureRepository been initialized ?")

        self.components = components

    def count(self):
        return len(self.programs)
