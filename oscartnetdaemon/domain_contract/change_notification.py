from dataclasses import dataclass

from oscartnetdaemon.domain_contract.value.base import BaseValue
from oscartnetdaemon.domain_contract.change_notification_scope_enum import ChangeNotificationScope


@dataclass
class ChangeNotification:
    variable_name: str
    new_value: BaseValue | None = None
    scope: ChangeNotificationScope = ChangeNotificationScope.Broadcast
