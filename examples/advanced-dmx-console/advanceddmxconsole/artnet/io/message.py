from dataclasses import dataclass

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage


@dataclass
class ArtnetIOMessage(AbstractIOMessage):
    channel: int
    value: int
