from dataclasses import dataclass

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration

from advanceddmxconsole.fixture.fixture_info import FixtureInfo
from advanceddmxconsole.fixture.fixture_type_info import FixtureTypeInfo


@dataclass
class ArtnetConfiguration(BaseConfiguration):
    universe: int
    target_nodes: list[str]
    fixture_types: dict[str, FixtureTypeInfo]
    fixtures: dict[str, FixtureInfo]
