from dataclasses import dataclass
from multiprocessing import Process

from oscartnetdaemon.domain_contract.service import Service


@dataclass
class ServiceBundle:
    service: Service
    process: Process | None = None
