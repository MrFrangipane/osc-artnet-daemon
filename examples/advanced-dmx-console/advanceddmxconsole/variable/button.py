from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.value.float import ValueFloat
from oscartnetdaemon.domain_contract.variable.float import VariableFloat

from advanceddmxconsole.io.message import ArtnetIOMessage
from advanceddmxconsole.variable_info import ArtnetVariableInfo
from advanceddmxconsole.variable.scribble_mixin import ArtnetScribbleMixin
from advanceddmxconsole.rename_me import RenameMe


class ArtnetButton(VariableFloat, ArtnetScribbleMixin):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion
        self.handle_scribble()

        if not self.value.value:
            return

        RenameMe().handle_button(info)

        if info.redirect:
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.name,
                new_value=ValueFloat(0.0)
            ))
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.redirect,
                new_value=ValueFloat(1.0)
            ))
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.redirect,
                new_value=ValueFloat(0.0)
            ))

    def handle_io_message(self, message: ArtnetIOMessage):
        """
        From IO to ChangeNotification
        """
        pass
