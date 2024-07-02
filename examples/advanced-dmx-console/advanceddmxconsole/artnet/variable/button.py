from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.value.float import ValueFloat
from oscartnetdaemon.domain_contract.variable.float import VariableFloat

from advanceddmxconsole.artnet.io.message import ArtnetIOMessage
from advanceddmxconsole.artnet.variable_info import ArtnetVariableInfo


class ArtnetButton(VariableFloat):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion
        if self.value.value and info.redirect:
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.name,
                value=ValueFloat(0.0)
            ))
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.redirect,
                value=ValueFloat(1.0)
            ))

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass