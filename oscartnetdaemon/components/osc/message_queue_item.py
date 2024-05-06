from dataclasses import dataclass

from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum


@dataclass
class OSCMessageQueueItem:
    client_ip: str  # fixme: use a discovery service
    client_port: int
    type: OSCWidgetTypeEnum
    address: str
    value: float
