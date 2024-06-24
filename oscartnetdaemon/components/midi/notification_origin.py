from dataclasses import dataclass

from oscartnetdaemon.components.domain.abstract_change_notificaton_origin import AbstractChangeNotificationOrigin


@dataclass
class MIDINotificationOrigin(AbstractChangeNotificationOrigin):
    implementation_name: str = 'MIDI'
