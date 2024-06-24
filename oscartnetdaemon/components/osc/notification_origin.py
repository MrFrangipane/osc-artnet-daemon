from dataclasses import dataclass

from oscartnetdaemon.components.domain.abstract_change_notificaton_origin import AbstractChangeNotificationOrigin


@dataclass
class OSCNotificationOrigin(AbstractChangeNotificationOrigin):
    remote_ip: tuple[int]
    implementation_name: str = 'OSC'
