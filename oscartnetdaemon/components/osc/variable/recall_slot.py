from oscartnetdaemon.components.osc.io.message import OSCMessage
from oscartnetdaemon.components.osc.recall.recall_group_repository import OSCRecallGroupRepository
from oscartnetdaemon.components.osc.variable_info import OSCVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.float import VariableFloat


# FIXME: RecallSlot concept exists in domain contract's VariableType enum, should it ?
class OSCRecallSlot(VariableFloat):

    def handle_change_notification(self, notification: ChangeNotification):
        """
        From ChangeNotification to IO
        """
        pass

    def handle_io_message(self, message: OSCMessage):
        """
        From IO to ChangeNotification
        """
        info: OSCVariableInfo = self.info  # FIXME type hint for autocompletion
        if not info.is_recall_slot or not message.osc_address.startswith(info.osc_address):
            return

        subcontrol = message.osc_address.split('/')[-1]

        if message.osc_value == 1 and subcontrol == 'save':
            OSCRecallGroupRepository().save_for_slot(info)

        elif message.osc_value == 1 and subcontrol == 'recall':
            OSCRecallGroupRepository().recall_for_slot(info)

        elif subcontrol == 'punch':
            OSCRecallGroupRepository().set_punch_for_slot(
                info,
                message.client_info,
                bool(message.osc_value)
            )
