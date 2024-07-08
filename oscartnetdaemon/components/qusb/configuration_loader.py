from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.components.qusb.argument_parser import parse_command_line_args
from oscartnetdaemon.components.qusb.configuration import QuSbConfiguration
from oscartnetdaemon.components.qusb.variable_info import QuSbVariableInfo


class QuSbConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self):
        self.filepaths = parse_command_line_args()
        self.variables: dict[str, QuSbVariableInfo] = dict()

    def load(self) -> QuSbConfiguration:
        return QuSbConfiguration(
            variable_infos=self.variables,
            host='192.168.20.4',
            port=51325
        )
