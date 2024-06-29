from dataclasses import dataclass

from oscartnetdaemon.components.osc.recall.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.components.osc.recall.memory_slot import OSCMemorySlot


@dataclass
class OSCRecallGroup:
    info: OSCRecallGroupInfo
    memory_slots: dict[str, OSCMemorySlot]
