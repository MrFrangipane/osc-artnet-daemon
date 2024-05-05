from dataclasses import dataclass


@dataclass
class OSCMessageQueueItem:
    client_ip: str  # fixme: use a discovery service
    client_port: int
    type: str  # fixme: enum here ?
    address: str
    value: float
