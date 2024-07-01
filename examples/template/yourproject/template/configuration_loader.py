from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from yourproject.template.argument_parser import parse_command_line_args
from yourproject.template.configuration import TemplateConfiguration
from yourproject.template.variable_info import TemplateVariableInfo


class TemplateConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self):
        self.filepaths = parse_command_line_args()
        self.variables: dict[str, TemplateVariableInfo] = dict()

    def load(self) -> TemplateConfiguration:
        return TemplateConfiguration(
            variable_infos=self.variables
        )
