from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase

from oscartnetdaemon.components.osc.entities.control_info import OSCControlInfo
from oscartnetdaemon.components.osc.entities.recall_group_info import OSCRecallGroupInfo


@dataclass_json(letter_case=LetterCase.KEBAB)
@dataclass
class OSCConfiguration:
    server_ip_address: str
    server_ip_address_autodetect: bool
    server_port: int
    controls: list[OSCControlInfo]
    recall_groups: list[OSCRecallGroupInfo]
