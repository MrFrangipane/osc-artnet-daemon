from multiprocessing import Queue
from typing import Type

from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable.abstract import AbstractVariable
from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.variable_type_enum import VariableType


class VariableRepository:

    def __init__(self, variable_types: dict[VariableType, Type[AbstractVariable]], notification_queue_out: "Queue[ChangeNotification]"):
        self.variable_types = variable_types
        self.variables: dict[str, AbstractVariable] = dict()
        self.notification_queue_out: Queue[ChangeNotification] = notification_queue_out

    def create_variables(self, configuration: BaseConfiguration, io_message_queue_out: "Queue[AbstractIOMessage]"):
        for variable_info in configuration.variable_infos.values():
            if variable_info.name in self.variables:
                raise NameError(f"Variable '{variable_info.name}' already exists")

            if variable_info.type not in self.variable_types:
                raise ValueError(
                    f"Variable type '{variable_info.type.name}' ({variable_info.name}) not registered for {configuration.__class__.__name__}"
                )

            new_variable = self.variable_types[variable_info.type](
                info=variable_info,
                io_message_queue_out=io_message_queue_out,
                notification_queue_out=self.notification_queue_out,
            )
            self.variables[variable_info.name] = new_variable

    def handle_change_notification(self, notification: ChangeNotification):
        """
        Calls associated Variable's handle_change_notification()
        Updates Variable's value beforehand if pertinent
        """
        variable = self.variables.get(notification.variable_name, None)
        if variable is not None:
            if not notification.ignore_value:
                variable.value = notification.value
            variable.handle_change_notification()

    def broadcast_io_message(self, message: AbstractIOMessage):
        """
        Asks all variables to handle the message
        """
        for variable in self.variables.values():
            variable.handle_io_message(message)

    def notify_all_variables(self):
        """
        Send a notification to all variables
        Useful when app starts or when new client connects
        """
        for variable in self.variables.values():
            self.notification_queue_out.put(ChangeNotification(
                variable_name=variable.info.name,
                value=variable.value
            ))
