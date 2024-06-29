from dataclasses import dataclass

from oscartnetdaemon.domain_contract.abstract_io_message import AbstractIOMessage
from oscartnetdaemon.components.new_osc.client_info import OSCClientInfo


@dataclass
class OSCMessage(AbstractIOMessage):  # TODO: do we need to inherit from AbstractIOMessage (and get .info ?) ?
    osc_address: str
    osc_value: float | str
    client_info: OSCClientInfo | None = None  # TODO: is this dangerous ?
