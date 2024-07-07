from dataclasses import dataclass, field
from multiprocessing import Queue

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable_repository import VariableRepository
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo
from oscartnetdaemon.domain_contract.base_shared_data import BaseSharedData


@dataclass
class ServiceComponents:
    configuration: BaseConfiguration | None = None
    registration_info: ServiceRegistrationInfo | None = None

    notification_queue_in: "Queue[ChangeNotification] | None" = None
    notification_queue_out: "Queue[ChangeNotification] | None" = None

    io_message_queue_in: "Queue[AbstractIOMessage] | None" = None
    io_message_queue_out: "Queue[AbstractIOMessage] | None" = None

    variable_repository: VariableRepository | None = None

    shared_data: BaseSharedData | None = None

    logging_queue: Queue = field(default_factory=Queue)
