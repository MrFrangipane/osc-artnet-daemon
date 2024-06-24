from dataclasses import dataclass

from oscartnetdaemon.components.domain.abstract_change_notificaton_origin import AbstractChangeNotificationOrigin
from oscartnetdaemon.components.domain.control.abstract import AbstractValue


@dataclass
class ChangeNotification:
    control_name: str
    value: AbstractValue
    origin: AbstractChangeNotificationOrigin
