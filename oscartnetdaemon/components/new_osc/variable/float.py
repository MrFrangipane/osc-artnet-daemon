from oscartnetdaemon.components.new_osc.io.message import OSCMessage
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


class OSCFloat(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        print(self.__class__.__name__, notification)

    def handle_io_message(self, message: OSCMessage):
        if message.osc_address == self.info.osc_address + '/fader':
            self.value.value = message.osc_value
            self.io_message_queue_out.put(OSCMessage(
                osc_address=self.info.osc_address + '/value',
                osc_value=int(self.value.value * 127)
            ))
