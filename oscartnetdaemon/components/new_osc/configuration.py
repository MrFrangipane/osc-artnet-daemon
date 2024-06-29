from dataclasses import dataclass

from oscartnetdaemon.components.new_osc.recall.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.domain_contract.base_configuration import BaseConfiguration


@dataclass
class OSCConfiguration(BaseConfiguration):
    server_ip_address: str
    server_ip_address_autodetect: bool
    server_port: int
    recall_groups: dict[str, OSCRecallGroupInfo]
