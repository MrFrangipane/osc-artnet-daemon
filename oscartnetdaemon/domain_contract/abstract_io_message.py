from dataclasses import dataclass

from oscartnetdaemon.domain_contract.variable_info import VariableInfo


@dataclass
class AbstractIOMessage:
    info: VariableInfo
