from abc import ABC, abstractmethod
from typing import Any

from oscartnetdaemon.components.domain.entities.control_update_origin_enum import DomainControlUpdateOrigin
from oscartnetdaemon.components.domain.repository import DomainControlRepository


class AbstractDomainControlsService(ABC):
    def __init__(self):
        self.control_repository: DomainControlRepository = None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def notify_update(self, origin: DomainControlUpdateOrigin, control_name: str, value: Any):
        pass
