from dataclasses import dataclass

from oscartnetdaemon.domain_contract.variable_info import VariableInfo


@dataclass
class BaseConfiguration:
    variable_infos: list[VariableInfo]
