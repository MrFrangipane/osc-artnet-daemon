from abc import ABC
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.value.text import ValueText
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable

from advanceddmxconsole.variable_info import ArtnetVariableInfo


class ArtnetScribbleMixin(AbstractVariable, ABC):
    def handle_scribble(self):
        info: ArtnetVariableInfo = self.info  # FIXME type hint for autocompletion

        if info.scribble_caption:
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.scribble_caption,
                new_value=ValueText(info.caption)
            ))

        if info.scribble_value:
            self.notification_queue_out.put(ChangeNotification(
                variable_name=info.scribble_value,
                new_value=ValueText(str(int(self.value.value * 255)))
            ))
