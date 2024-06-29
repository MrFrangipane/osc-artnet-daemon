from oscartnetdaemon.components.osc.io.message import OSCMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from oscartnetdaemon.components.osc.variable_info import OSCVariableInfo


class OSCFader(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        info: OSCVariableInfo = self.info  # FIXME type hint for autocompletion

        self.io_message_queue_out.put(OSCMessage(
            osc_address=info.osc_address + '/value',
            osc_value=int(self.value.value * 127)
        ))
        self.io_message_queue_out.put(OSCMessage(
            osc_address=info.osc_address + '/fader',
            osc_value=self.value.value
        ))
        self.io_message_queue_out.put(OSCMessage(
            osc_address=info.osc_address + '/caption',
            osc_value=info.caption
        ))

    def handle_io_message(self, message: OSCMessage):
        """
        From IO to ChangeNotification
        """
        info: OSCVariableInfo = self.info  # FIXME type hint for autocompletion
        if message.osc_address == info.osc_address + '/fader':
            self.value.value = message.osc_value
            self.notify_change()
