from dataclasses import dataclass

from oscartnetdaemon.components.qusb.parameter_type_enum import QuSbParameterType
from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage


@dataclass
class QuSbIOMessage(AbstractIOMessage):
    channel: int = None
    parameter: QuSbParameterType = None
    value: int = None
    is_complete: bool = False
