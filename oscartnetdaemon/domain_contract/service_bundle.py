from dataclasses import dataclass
from multiprocessing import Process

from oscartnetdaemon.domain_contract.service import Service
from oscartnetdaemon.domain_contract.service_registration_info import ServiceRegistrationInfo


@dataclass
class ServiceBundle:
    service: Service
    registration_info: ServiceRegistrationInfo
    process: Process | None = None
