from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from oscartnetdaemon.components.qusb.io.message import QuSbIOMessage
from oscartnetdaemon.components.qusb.variable_info import QuSbVariableInfo
from oscartnetdaemon.components.qusb.parameter_type_enum import QuSbParameterType


class QuSbFader(VariableFloat):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: QuSbVariableInfo = self.info  # FIXME type hint for autocompletion
        if info.channel == -1:
            return

        self.io_message_queue_out.put(QuSbIOMessage(
            channel=info.channel,
            parameter=QuSbParameterType.Fader,
            value=int(self.value.value * 127),
            is_complete=True
        ))

    def handle_io_message(self, message: QuSbIOMessage):
        """
        From IO to ChangeNotification
        """
        info: QuSbVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.channel != message.channel or message.parameter != QuSbParameterType.Fader:
            return

        self.value.value = float(message.value) / 127.0
        self.notify_change()
