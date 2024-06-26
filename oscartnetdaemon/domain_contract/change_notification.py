from dataclasses import dataclass

from oscartnetdaemon.domain_contract.value.base import BaseValue
from oscartnetdaemon.domain_contract.variable_info import VariableInfo


@dataclass
class ChangeNotification:
    info: VariableInfo
    value: BaseValue | None
    ignore_value: bool = False  # FIXME: could this be more elegant ? (two subclasses of a BaseNotification ?)
