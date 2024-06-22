from oscartnetdaemon.components.components_singleton import Components
from oscartnetdaemon.components.midi.control_repository import MIDIControlRepository
from oscartnetdaemon.entities.midi.context import MIDIContext
from oscartnetdaemon.entities.midi.control_update_info import MIDIControlUpdateInfo
from oscartnetdaemon.entities.midi.message import MIDIMessage


class MIDIMessageHandler:
    def __init__(self, control_repository: MIDIControlRepository):
        self.control_repository = control_repository

    def handle(self, message: MIDIMessage, context: MIDIContext):
        for control in self.control_repository.controls.values():
            if control.complies_with(message, context) and control.handle_message(message, context):
                Components().midi_service.notify_update(MIDIControlUpdateInfo(
                    control_name=control.info.name,
                    mapped_to=control.info.mapped_to,
                    value=control.value
                ))
