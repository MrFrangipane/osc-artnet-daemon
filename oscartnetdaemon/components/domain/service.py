from typing import Type

from oscartnetdaemon.components.configuration.entities.configuration import ConfigurationInfo
from oscartnetdaemon.components.domain.control.repository import DomainControlRepository
from oscartnetdaemon.components.domain.entities.control_info import DomainControlInfo
from oscartnetdaemon.components.implementation.abstract import AbstractImplementation
from oscartnetdaemon.components.implementation.repository import ImplementationRepository


class DomainService:

    def __init__(self, configuration_info: ConfigurationInfo):
        self._configuration_info = configuration_info
        self._control_repository = DomainControlRepository()
        self.implementation_repository = ImplementationRepository(self._configuration_info)

    def register_implementation_type(self, implementation_type: Type[AbstractImplementation]):
        self.implementation_repository.register_implementation_type(implementation_type)

    def create_controls(self, infos: dict[str, DomainControlInfo]):
        self._control_repository.create_controls(infos)

    def run_forever(self):
        self.implementation_repository.start_all()

        while True:
            for notification in self.implementation_repository.get_notifications():
                self._control_repository.controls[notification.control_name].value = notification.value
                self.implementation_repository.put_notification(notification)

    def stop(self):
        self.implementation_repository.terminate_all()
