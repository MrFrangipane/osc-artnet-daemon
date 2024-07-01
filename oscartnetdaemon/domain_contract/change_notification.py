from dataclasses import dataclass

from oscartnetdaemon.domain_contract.value.base import BaseValue


@dataclass
class ChangeNotification:
    variable_name: str
    value: BaseValue | None = None
    ignore_value: bool = False  # FIXME: could this be more elegant ? (two subclasses of a BaseNotification ?)
