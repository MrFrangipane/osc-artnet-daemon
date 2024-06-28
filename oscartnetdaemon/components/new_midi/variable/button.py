from oscartnetdaemon.components.new_midi.compliance_checker import MIDIComplianceChecker
from oscartnetdaemon.components.new_midi.context import MIDIContext
from oscartnetdaemon.components.new_midi.io.message import MIDIMessage
from oscartnetdaemon.components.new_midi.io.message_type_enum import MIDIMessageType
from oscartnetdaemon.components.new_midi.page_direction_enum import MIDIPageDirection
from oscartnetdaemon.components.new_midi.variable_info import MIDIVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class MIDIButton(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: MIDIVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.is_page_button and self.value.value == 1:
            self._handle_pagination_change(info)

        elif info.is_layer_button and self.value.value == 1:
            self._handle_layer_change(info)

        if MIDIComplianceChecker.with_current_layer(info) and MIDIComplianceChecker.with_current_page(info):
            self.io_message_queue_out.put(MIDIMessage(
                channel=info.midi_parsing.channel,
                device_name=info.device_name,
                type=MIDIMessageType.NoteOn,
                note=info.midi_parsing.note,
                velocity=int(self.value.value * 127)
            ))

    def handle_io_message(self, message: MIDIMessage):
        """
        From IO to ChangeNotification
        """
        if not MIDIComplianceChecker.with_io_message(self.info, message):
            return

        self.value.value = float(message.velocity / 127.0)
        self.notify_change()

    def _handle_pagination_change(self, info: MIDIVariableInfo):
        pagination_info = MIDIContext().pagination_infos[info.pagination_name]

        if info.page_direction == MIDIPageDirection.Up:
            page_changed = pagination_info.up()
        else:
            page_changed = pagination_info.down()

        if page_changed:
            for variable_info in pagination_info.variables[pagination_info.current_page]:
                if not MIDIComplianceChecker.with_current_layer(variable_info):
                    continue
                self.notification_queue_out.put(ChangeNotification(
                    info=variable_info,
                    value=None,
                    ignore_value=True
                ))

    def _handle_layer_change(self, info: MIDIVariableInfo):
        layer_group_info = MIDIContext().layer_group_infos[info.layer_group_name]
        layer_info = layer_group_info.layers[info.layer_name]

        if layer_info.name != layer_group_info.current_layer_name:
            layer_group_info.current_layer_name = layer_info.name

            # TODO find a way to radio-illuminate layer group's buttons

            for variable_info in layer_info.variables:
                self.notification_queue_out.put(ChangeNotification(
                    info=variable_info,
                    value=None,
                    ignore_value=True
                ))
