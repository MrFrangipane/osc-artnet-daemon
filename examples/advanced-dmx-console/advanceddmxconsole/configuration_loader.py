import yaml

from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader

from advanceddmxconsole.argument_parser import parse_command_line_args
from advanceddmxconsole.configuration import ArtnetConfiguration
from advanceddmxconsole.fixture.fixture_info import FixtureInfo
from advanceddmxconsole.fixture.fixture_type_info import FixtureTypeInfo
from advanceddmxconsole.variable_info import ArtnetVariableInfo


class ArtnetConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self):
        self.filepaths, self.universe, self.target_nodes = parse_command_line_args()
        self.variables: dict[str, ArtnetVariableInfo] = dict()
        self.fixture_types: dict[str, FixtureTypeInfo] = dict()
        self.fixtures: dict[str, FixtureInfo] = dict()
        self.file_content: dict = dict()

    def load(self) -> ArtnetConfiguration:
        self.file_content = dict()
        self.variables = dict()
        self.fixture_types = dict()
        self.fixtures = dict()

        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                self.file_content.update(yaml.safe_load(file))

        for variable_dict in self.file_content['variables']:
            if variable_dict['name'] in self.variables:
                raise ValueError(f"MIDI Variable '{variable_dict['name']}' already assigned")

            self.variables[variable_dict['name']] = ArtnetVariableInfo.from_dict(variable_dict)

        for fixture_type in self.file_content['fixtures-types']:
            new_fixture_type: FixtureTypeInfo = FixtureTypeInfo.from_dict(fixture_type)
            if new_fixture_type.name in self.fixture_types:
                raise ValueError(f"FixtureType name already defined '{new_fixture_type.name}'")

            self.fixture_types[new_fixture_type.name] = new_fixture_type

        for fixture in self.file_content['fixtures']:
            type_name = fixture['type']
            if type_name not in self.fixture_types:
                raise ValueError(f"FixtureType not found '{type_name}'")

            fixture['type'] = self.fixture_types[type_name]
            new_fixture: FixtureInfo = FixtureInfo.from_dict(fixture)
            if new_fixture.name in self.fixture_types:
                raise ValueError(f"FixtureType name already defined '{new_fixture.name}'")

            self.fixtures[new_fixture.name] = new_fixture

        return ArtnetConfiguration(
            universe=self.universe,
            target_nodes=self.target_nodes,
            variable_infos=self.variables,
            fixture_types=self.fixture_types,
            fixtures=self.fixtures
        )
