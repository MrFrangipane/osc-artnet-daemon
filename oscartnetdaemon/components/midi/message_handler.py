from multiprocessing import Queue

from oscartnetdaemon.components.domain.change_notification import ChangeNotification
from oscartnetdaemon.components.midi.control_repository import MIDIControlRepository
from oscartnetdaemon.components.midi.entities.context import MIDIContext
from oscartnetdaemon.components.midi.entities.message import MIDIMessage
from oscartnetdaemon.components.midi.notification_origin import MIDINotificationOrigin


class MIDIMessageHandler:
    def __init__(self, control_repository: MIDIControlRepository, notification_queue: Queue):
        self.control_repository = control_repository
        self.notification_queue = notification_queue

    def handle(self, message: MIDIMessage, context: MIDIContext):
        for midi_control in self.control_repository.controls.values():
            if midi_control.complies_with(message, context) and midi_control.handle_message(message, context):
                if midi_control.info.mapped_to:
                    self.notification_queue.put(ChangeNotification(
                        control_name=midi_control.info.mapped_to,
                        value=midi_control.value,
                        origin=MIDINotificationOrigin()
                    ))
                else:
                    print(midi_control.info)
