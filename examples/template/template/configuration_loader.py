from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from template.configuration import TemplateConfiguration
from template.variable_info import TemplateVariableInfo


class TemplateConfigurationLoader(AbstractConfigurationLoader):
    """
    At least returns a BaseConfiguration object
    Subtype of BaseConfiguration can be created to load additional IO specific configuration
    """

    def __init__(self, filepaths):
        super().__init__(filepaths)
        self.variables: dict[str, TemplateVariableInfo] = dict()

    def load(self) -> TemplateConfiguration:
        return TemplateConfiguration(
            variable_infos=self.variables
        )
