from dataclasses import dataclass
from typing import Type

from oscartnetdaemon.domain_contract.abstract_configuration_loader import AbstractConfigurationLoader
from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType
from oscartnetdaemon.domain_contract.variable_repository import VariableRepository


@dataclass
class ServiceRegistrationInfo:
    configuration_loader: AbstractConfigurationLoader
    io_type: Type[AbstractIO]
    variable_types: dict[VariableType, Type[AbstractVariable]]
    variable_repository_type: Type[VariableRepository] | None = None
