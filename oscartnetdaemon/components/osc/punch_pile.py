from oscartnetdaemon.components.osc.recall_group import OSCRecallGroup, OSCMemorySlot
from oscartnetdaemon.entities.osc.client_info import OSCClientInfo


class PunchPile:
    _base_slot_name = "###$$$"  # FIXME: make this name reserved (warn user if present in mapping YML file)

    def __init__(self, info: OSCClientInfo):
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
                for widget in recall_group.widgets:
                    base_memory_slot.widgets_values[widget.info.osc_address] = widget.get_values()

            # Other punches, save new punch
            self.pile.append(memory_slot.osc_address)
            self.memory_slots[memory_slot.osc_address] = memory_slot

            # Apply
            for widget in recall_group.widgets:
                values = memory_slot.widgets_values.get(widget.info.osc_address, None)
                if values is not None:
                    widget.set_values(values)

        else:
            self.pile.remove(memory_slot.osc_address)
            previous_punch = self.pile[-1]
            previous_memory_slot = self.memory_slots[previous_punch]
            for widget in recall_group.widgets:
                values = previous_memory_slot.widgets_values.get(widget.info.osc_address, None)
                if values is not None:
                    widget.set_values(values)
