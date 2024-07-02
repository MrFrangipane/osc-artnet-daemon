import yaml

from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader

from advanceddmxconsole.artnet.variable_info import ArtnetVariableInfo
from advanceddmxconsole.argument_parser import parse_command_line_args
from advanceddmxconsole.configuration import ArtnetConfiguration


class ArtnetConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self):
        self.filepaths, self.universe, self.target_nodes = parse_command_line_args()
        self.variables: dict[str, ArtnetVariableInfo] = dict()
        self.file_contents: list[dict] = list()

    def load(self) -> ArtnetConfiguration:
        for filepath in self.filepaths:
            with open(filepath, 'r') as file:
                self.file_contents.append(yaml.safe_load(file))

        for file_content in self.file_contents:
            for variable_dict in file_content['variables']:
                if variable_dict['name'] in self.variables:
                    raise ValueError(f"MIDI Variable '{variable_dict['name']}' already assigned")

                self.variables[variable_dict['name']] = ArtnetVariableInfo.from_dict(variable_dict)

        return ArtnetConfiguration(
            universe=self.universe,
            target_nodes=self.target_nodes,
            variable_infos=self.variables
        )
