from typing import Any

from dataclasses import dataclass

from oscartnetdaemon.midi_osc_test_bridge.domain.abstract_change_notificaton_origin import AbstractChangeNotificationOrigin


@dataclass
class ChangeNotification:
    control_name: str
    origin: AbstractChangeNotificationOrigin
    value: Any
