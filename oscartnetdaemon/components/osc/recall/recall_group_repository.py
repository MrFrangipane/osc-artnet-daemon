from copy import copy
from multiprocessing import Queue

from oscartnetdaemon.components.osc.client_info import OSCClientInfo
from oscartnetdaemon.components.osc.recall.memory_slot import OSCMemorySlot
from oscartnetdaemon.components.osc.recall.punch_pile import OSCPunchPile
from oscartnetdaemon.components.osc.recall.recall_group import OSCRecallGroup
from oscartnetdaemon.components.osc.recall.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.components.osc.variable_info import OSCVariableInfo
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification
from oscartnetdaemon.domain_contract.variable_repository import VariableRepository
from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


class OSCRecallGroupRepository(metaclass=SingletonMetaclass):
    def __init__(self):
        self.recall_groups: dict[str, OSCRecallGroup] = dict()
        self._punch_piles: dict[bytes, OSCPunchPile] = dict()
        self.variable_repository: VariableRepository | None = None
        self.notification_queue_out: Queue[ChangeNotification] | None = None

    def create_groups(self, recall_group_infos: dict[str, OSCRecallGroupInfo]):
        self.recall_groups = dict()
        for group_name, group_info in recall_group_infos.items():
            self.recall_groups[group_name] = OSCRecallGroup(
                info=group_info,
                memory_slots={
                    slot_variable_info.name: OSCMemorySlot(slot_variable_info.name)
                    for slot_variable_info in group_info.recall_slots.values()
                }
            )

    #
    # REGISTRATION
    def register_client(self, client_info: OSCClientInfo):
        if self._punch_piles.get(client_info.id, None) is None:
            self._punch_piles[client_info.id] = OSCPunchPile(
                notification_queue_out=self.notification_queue_out,
                variable_repository=self.variable_repository
            )

    def unregister_client(self, client_info: OSCClientInfo):
        # Do nothing to keep punches between registrations
        pass

    #
    # SAVE / RECALL / PUNCH
    def save_for_slot(self, variable_slot: OSCVariableInfo):
        recall_group = self.recall_groups[variable_slot.recall_group_name]
        slot = recall_group.memory_slots[variable_slot.name]

        for variable_info in recall_group.info.target_variables.values():
            variable = self.variable_repository.variables[variable_info.name]
            slot.values[variable_info.name] = copy(variable.value)

    def recall_for_slot(self, variable_slot: OSCVariableInfo):
        # FIXME: find a way to notify only OSC clients ? (or unification in domain contract will remove the problem ?)
        recall_group = self.recall_groups[variable_slot.recall_group_name]
        slot = recall_group.memory_slots[variable_slot.name]

        for variable_info in recall_group.info.target_variables.values():
            self.notification_queue_out.put(ChangeNotification(
                variable_name=variable_info.name,
                new_value=copy(slot.values[variable_info.name])
            ))

    def set_punch_for_slot(self, variable_slot: OSCVariableInfo, client_info: OSCClientInfo, is_punch: bool):
        if client_info is None:
            print(f"Trying to punch from an unregistered client, aborting")
            return

        recall_group = self.recall_groups[variable_slot.recall_group_name]
        memory_slot = recall_group.memory_slots[variable_slot.name]
        self._punch_piles[client_info.id].set_punch(recall_group, memory_slot, is_punch)
