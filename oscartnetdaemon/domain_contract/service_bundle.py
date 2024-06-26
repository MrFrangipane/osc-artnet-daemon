from dataclasses import dataclass
from multiprocessing import Process, Queue

from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.service import Service


@dataclass
class ServiceBundle:
    service: Service
    process: Process | None = None
    # notification_queue_in: "Queue[ChangeNotification] | None" = None
    # notification_queue_out: "Queue[ChangeNotification] | None" = None
