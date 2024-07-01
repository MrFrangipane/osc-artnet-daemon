from oscartnetdaemon.domain_contract.variable.float import VariableFloat
from yourproject.template.io.message import TemplateMessage
from yourproject.template.variable_info import TemplateVariableInfo


class TemplateFader(VariableFloat):

    def handle_change_notification(self):
        """
        From ChangeNotification to IO
        """
        info: TemplateVariableInfo = self.info  # FIXME type hint for autocompletion

        # Do stuff here

    def handle_io_message(self, message: TemplateMessage):
        """
        From IO to ChangeNotification
        """
        info: TemplateVariableInfo = self.info  # FIXME type hint for autocompletion

        # Do stuff, update value here

        self.notify_change()
