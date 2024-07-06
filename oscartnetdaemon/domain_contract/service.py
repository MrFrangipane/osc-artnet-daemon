import time
import logging
from multiprocessing import Event, Queue

from oscartnetdaemon.domain_contract.abstract_io import AbstractIO
from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.service_components import ServiceComponents
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.variable_repository import VariableRepository


_logger = logging.getLogger(__name__)


class Service:
    def __init__(self, registration_info: ServiceRegistrationInfo):
        self.components = ServiceComponents()
        self.configuration_loader = registration_info.configuration_loader
        self.configuration: BaseConfiguration | None = None

        self.notification_queue_in: Queue[ChangeNotification] = Queue()
        self.notification_queue_out: Queue[ChangeNotification] = Queue()

        self._make_variable_repository(registration_info)

        self.io: AbstractIO | None = None
        self.io_type = registration_info.io_type
        self.io_message_queue_in: Queue[AbstractIOMessage] = Queue()
        self.io_message_queue_out: Queue[AbstractIOMessage] = Queue()

        self.startup_done = Event()

    def _make_variable_repository(self, registration_info: ServiceRegistrationInfo):
        if registration_info.variable_repository_type is not None:
            if not issubclass(registration_info.variable_repository_type, VariableRepository):
                raise ValueError('Variable repository type is not a subclass of VariableRepository')

            _logger.info(f"{registration_info.io_type.__name__} uses variable repository {registration_info.variable_repository_type.__name__}")
            variable_repository_type = registration_info.variable_repository_type
        else:
            variable_repository_type = VariableRepository

        self.variable_repository = variable_repository_type(
            variable_types=registration_info.variable_types,
            notification_queue_out=self.notification_queue_out
        )
        self.components.variable_repository = self.variable_repository

    def initialize(self):
        self.configuration = self.configuration_loader.load()
        self.variable_repository.create_variables(
            configuration=self.configuration,
            io_message_queue_out=self.io_message_queue_out
        )
        self.components.configuration = self.configuration
        self.components.io_message_queue_in = self.io_message_queue_in
        self.components.io_message_queue_out = self.io_message_queue_out
        self.components.notification_queue_in = self.notification_queue_in
        self.components.notification_queue_out = self.notification_queue_out

        self.io = self.io_type(self.components)

    def exec(self):
        """
        Entry point for Service's dedicated multiprocessing.Process
        """
        self.initialize()
        self.io.start()
        self.startup_done.set()
        self.variable_repository.notify_all_variables()

        try:
            while True:
                #
                # Notifications
                while not self.notification_queue_in.empty():
                    notification = self.notification_queue_in.get()
                    self.variable_repository.handle_change_notification(notification)
                #
                # IO
                while not self.io_message_queue_in.empty():
                    message = self.io_message_queue_in.get()
                    self.variable_repository.broadcast_io_message(message)

                while not self.io_message_queue_out.empty():
                    message = self.io_message_queue_out.get()
                    self.io.send_io_message(message)

                time.sleep(0.01)

        except KeyboardInterrupt:
            pass

        except Exception as e:
            raise

        finally:
            self.shutdown()

    def shutdown(self):
        self.io.shutdown()
