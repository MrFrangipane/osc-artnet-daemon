from oscartnetdaemon.components.midi.control_repository import MIDIControlRepository
from oscartnetdaemon.entities.midi.context import MIDIContext
from oscartnetdaemon.entities.midi.message import MIDIMessage


class MIDIMessageHandler:
    def __init__(self, control_repository: MIDIControlRepository):
        self.control_repository = control_repository

    def handle(self, message: MIDIMessage, context: MIDIContext):
        for control in self.control_repository.controls.values():
            if control.complies_with(message, context):
                update_info = control.handle_message(message, context)
                if update_info is not None:
                    print(update_info)
