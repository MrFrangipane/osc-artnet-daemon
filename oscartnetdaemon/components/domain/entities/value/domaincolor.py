from oscartnetdaemon.components.domain.entities.value.abstract import AbstractDomainValue


class DomainColor(AbstractDomainValue):
    h: float
    s: float
    l: float
