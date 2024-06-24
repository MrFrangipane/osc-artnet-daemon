from oscartnetdaemon.components.domain.entities.control_info import DomainControlInfo
from oscartnetdaemon.components.domain.entities.value.abstract import AbstractDomainValue


# FIXME : will we need control subtypes ? This seems to be sufficient
class AbstractDomainControl:

    def __init__(self, info: DomainControlInfo):
        self.info = info
        self.value: AbstractDomainValue = None

    def set_value(self, value: AbstractDomainValue):
        self.value = value
        print(f"Value set {self.info.name}={value}")
