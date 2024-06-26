from oscartnetdaemon.components.new_osc.io.message import OSCMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class OSCFader(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        self.value.value = notification.value.value

        self.io_message_queue_out.put(OSCMessage(
            osc_address=self.info.osc_address + '/value',
            osc_value=int(self.value.value * 127)
        ))
        self.io_message_queue_out.put(OSCMessage(
            osc_address=self.info.osc_address + '/fader',
            osc_value=self.value.value
        ))

    def handle_io_message(self, message: OSCMessage):
        """
        From IO to ChangeNotification
        """
        if message.osc_address == self.info.osc_address + '/fader':
            self.value.value = message.osc_value
            self.notification_queue_out.put(ChangeNotification(
                info=self.info,
                value=self.value
            ))
