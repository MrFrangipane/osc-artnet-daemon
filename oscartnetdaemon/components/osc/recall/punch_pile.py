from copy import copy
from multiprocessing import Queue

from oscartnetdaemon.components.osc.recall.memory_slot import OSCMemorySlot
from oscartnetdaemon.components.osc.recall.recall_group import OSCRecallGroup
from oscartnetdaemon.domain_contract.variable_repository import VariableRepository
from oscartnetdaemon.domain_contract.change_notification import ChangeNotification


class OSCPunchPile:
    _base_slot_name = "###$$$"  # FIXME: make this name reserved (warn user if present in mapping YML file)

    def __init__(self, notification_queue_out: "Queue[ChangeNotification]", variable_repository: VariableRepository):
        # FIXME create an API for variable repository and notification broadcasting
        self.notification_queue_out = notification_queue_out
        self.variable_repository = variable_repository
        self.memory_slots: dict[str, OSCMemorySlot] = dict()
        self.pile: list[str] = [self._base_slot_name]

    def set_punch(self, recall_group: OSCRecallGroup, memory_slot: OSCMemorySlot, is_punch):
        if is_punch:
            # 1st punch in the pile, save current state
            if self.pile == [self._base_slot_name]:
                # Create slot if not exists
                if self.memory_slots.get(self._base_slot_name, None) is None:
                    base_memory_slot = OSCMemorySlot("BaseMemorySlot")
                    self.memory_slots[self._base_slot_name] = base_memory_slot

                # Save state to slot
                base_memory_slot = self.memory_slots[self._base_slot_name]
                for variable_info in recall_group.info.target_variables.values():
                    variable = self.variable_repository.variables[variable_info.name]
                    base_memory_slot.values[variable_info.name] = copy(variable.value)

            # Other punches, save new punch
            self.pile.append(memory_slot.name)
            self.memory_slots[memory_slot.name] = memory_slot

            # Apply
            for variable_info in recall_group.info.target_variables.values():
                value = memory_slot.values.get(variable_info.name, None)
                if value is not None:
                    self.notification_queue_out.put(ChangeNotification(
                        info=variable_info,
                        value=copy(value)
                    ))

        else:
            self.pile.remove(memory_slot.name)
            previous_punch = self.pile[-1]
            previous_memory_slot = self.memory_slots[previous_punch]
            for variable_info in recall_group.info.target_variables.values():
                value = previous_memory_slot.values.get(variable_info.name, None)
                if value is not None:
                    self.notification_queue_out.put(ChangeNotification(
                        info=variable_info,
                        value=copy(value)
                    ))
