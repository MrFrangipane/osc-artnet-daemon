from multiprocessing import Queue
from typing import Type

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable
from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


class VariableRepository:

    def __init__(self, variable_types: dict[VariableType, Type[AbstractVariable]]):
        self.variable_types = variable_types
        self.variables: dict[str, AbstractVariable] = dict()

    def create_variables(self, configuration: BaseConfiguration, message_queue_out: "Queue[AbstractIOMessage]", notification_queue_out: "Queue[ChangeNotification]"):
        for variable_info in configuration.variable_infos.values():
            if variable_info.name in self.variables:
                raise NameError(f"Variable '{variable_info.name}' already exists")

            if variable_info.type not in self.variable_types:
                raise ValueError(
                    f"Variable type '{variable_info.type.name}' not registered for {configuration.__class__.__name__}"
                )

            new_variable = self.variable_types[variable_info.type](
                info=variable_info,
                io_message_queue_out=message_queue_out,
                notification_queue_out=notification_queue_out,
            )
            self.variables[variable_info.name] = new_variable

    def forward_change_notification(self, notification: ChangeNotification):
        variable = self.variables.get(notification.info.name, None)
        if variable is not None:
            variable.handle_change_notification(notification)

    def broadcast_io_message(self, message: AbstractIOMessage):
        """
        Asks all variables to handle the message
        """
        for variable in self.variables.values():
            variable.handle_io_message(message)
