from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.domain_contract.variable_info import VariableInfo
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


class AAConfigurationLoader(AbstractConfigurationLoader):

    def __init__(self, filepath):
        super().__init__(filepath)

    def load(self) -> BaseConfiguration:
        return BaseConfiguration(
            variable_infos=[
                VariableInfo(name="FADER_A", type=VariableType.Float),
                VariableInfo(name="FADER_B", type=VariableType.Float),
            ]
        )
