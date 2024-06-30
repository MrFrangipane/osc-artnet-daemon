from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from artnet.argument_parser import parse_command_line_args
from artnet.configuration import ArtnetConfiguration
from artnet.variable_info import ArtnetVariableInfo


class ArtnetConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self):
        self.filepaths = parse_command_line_args()
        self.variables: dict[str, ArtnetVariableInfo] = dict()

    def load(self) -> ArtnetConfiguration:
        return ArtnetConfiguration(
            variable_infos=self.variables
        )
