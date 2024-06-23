from dataclasses import dataclass

from oscartnetdaemon.midi_osc_test_bridge.domain.abstract_change_notificaton_origin import AbstractChangeNotificationOrigin
from oscartnetdaemon.midi_osc_test_bridge.domain.controls import AbstractControlValue


@dataclass
class ChangeNotification:
    control_name: str
    value: AbstractControlValue
    origin: AbstractChangeNotificationOrigin
