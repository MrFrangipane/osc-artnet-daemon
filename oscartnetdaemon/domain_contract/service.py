from multiprocessing import Queue

from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_repository import VariableRepository


class Service:
    def __init__(self, registration_info: ServiceRegistrationInfo):
        self.configuration_loader = registration_info.configuration_loader
        self.configuration: BaseConfiguration | None = None

        self.variable_repository = VariableRepository(registration_info.variable_types)

        self.notification_queue_in: Queue[ChangeNotification] = Queue()
        self.notifications_queue_out: Queue[ChangeNotification] = Queue()

        self.io: AbstractIO | None = None
        self.io_type = registration_info.io_type
        self.io_message_queue_in: Queue[AbstractIOMessage] = Queue()
        self.io_message_queue_out: Queue[AbstractIOMessage] = Queue()

    def initialize(self):
        self.configuration = self.configuration_loader.load()
        self.variable_repository.create_variables(self.configuration, self.io_message_queue_out)
        self.io = self.io_type(self.io_message_queue_in, self.io_message_queue_out)

    def exec(self):
        self.io.start()

        while True:
            while not self.notification_queue_in.empty():
                notification = self.notification_queue_in.get()
                self.variable_repository.forward_change_notification(notification)

            while not self.io_message_queue_in.empty():
                message = self.io_message_queue_in.get()
                self.variable_repository.forward_io_message(message)

    def shutdown(self):
        self.io.shutdown()
