from dataclasses import dataclass

from oscartnetdaemon.components.qusb.parameter_type_enum import QuSbParameterType
from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.change_notification_scope_enum import ChangeNotificationScope


@dataclass
class QuSbIOMessage(AbstractIOMessage):
    channel: int = None
    parameter: QuSbParameterType = None
    value: int = None
    is_complete: bool = False
    scope: ChangeNotificationScope = ChangeNotificationScope.Foreign
