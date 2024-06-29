from dataclasses import dataclass

from oscartnetdaemon.domain_contract.variable_info import VariableInfo


@dataclass
class BaseConfiguration:
    """Contains at least all variable infos for a given IO implementation"""
    variable_infos: dict[str, VariableInfo]
