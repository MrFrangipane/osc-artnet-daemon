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

    def create_variables(self, configuration: BaseConfiguration, message_queue: "Queue[AbstractIOMessage]"):
        for variable_info in configuration.variable_infos:
            if variable_info.name in self.variables:
                raise NameError(f"Variable '{variable_info.name}' already exists")

            new_variable = self.variable_types[variable_info.type](
                info=variable_info,
                io_message_queue_out=message_queue
            )
            self.variables[variable_info.name] = new_variable

    def forward_change_notification(self, notification: ChangeNotification):
        self.variables[notification.info.name].handle_change_notification(notification)

    def forward_io_message(self, message: AbstractIOMessage):
        self.variables[message.info.name].handle_implementation_message(message)
