from dataclasses import dataclass

from oscartnetdaemon.midi_osc_test_bridge.domain.abstract_change_notificaton_origin import AbstractChangeNotificationOrigin


@dataclass
class OSCNotificationOrigin(AbstractChangeNotificationOrigin):
    remote_ip: tuple[int]
