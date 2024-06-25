import logging

from oscartnetdaemon.components.osc.recall.abstract_recall_groups_repository import AbstractOSCRecallGroupsRepository
from oscartnetdaemon.components.osc.recall.punch_pile import PunchPile
from oscartnetdaemon.components.osc.entities.recall_group import OSCRecallGroup, OSCMemorySlot
from oscartnetdaemon.components.osc.controls.abstract import OSCAbstractControl

from oscartnetdaemon.components.osc.entities.client_info import OSCClientInfo
from oscartnetdaemon.components.osc.entities.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.components.osc.entities.control_type_enum import OSCControlType


_logger = logging.getLogger(__name__)


# fixme: move work to OSCRecallGroup objects ?
class OSCRecallGroupsRepository(AbstractOSCRecallGroupsRepository):

    def __init__(self):
        self._recall_groups: dict[str, OSCRecallGroup] = dict()
        self._punch_piles: dict[bytes, PunchPile] = dict()

    def create_groups(self, controls: list[OSCAbstractControl], recall_group_infos: list[OSCRecallGroupInfo]):
        self._recall_groups = dict()
        all_controls_indexed: dict[str: OSCAbstractControl] = {control.info.osc_address: control for control in controls}
        assigned_memory_slots_addresses: list[str] = list()

        for group_info in recall_group_infos:
            group_controls = [
                all_controls_indexed[osc_address]
                for osc_address in group_info.controls_osc_addresses
                if not all_controls_indexed[osc_address].info.type == OSCControlType.RecallSlot
            ]

            memory_slots: {str: OSCMemorySlot} = dict()
            for osc_address in group_info.controls_osc_addresses:
                if all_controls_indexed[osc_address].info.type != OSCControlType.RecallSlot:
                    continue

                if osc_address in assigned_memory_slots_addresses:
                    raise ValueError(f"Memory slot '{osc_address}' already in use in a Recall Group")

                memory_slots[osc_address] = OSCMemorySlot(osc_address=osc_address)
                assigned_memory_slots_addresses.append(osc_address)

            new_recall_group = OSCRecallGroup(
                name=group_info.name,
                controls=group_controls,
                memory_slots=memory_slots
            )

            for osc_address in memory_slots:
                self._recall_groups[osc_address] = new_recall_group

    def register_client(self, client_info: OSCClientInfo):
        if self._punch_piles.get(client_info.id, None) is None:
            self._punch_piles[client_info.id] = PunchPile(client_info)

    def unregister_client(self, client_info: OSCClientInfo):
        # Do nothing to keep punches between registrations
        pass

    def save_for_slot(self, osc_address: str):
        recall_group = self._recall_groups[osc_address]
        for control in recall_group.controls:
            recall_group.memory_slots[osc_address].controls_values[control.info.osc_address] = control.get_values()

    def recall_for_slot(self, osc_address: str):
        recall_group = self._recall_groups[osc_address]
        for control in recall_group.controls:
            values = recall_group.memory_slots[osc_address].controls_values.get(control.info.osc_address, None)
            if values is not None:
                control.set_values(values)

    def set_punch_for_slot(self, client_info: OSCClientInfo, osc_address: str, is_punch: bool):
        if client_info is None:
            _logger.warning(f"Trying to punch from an unregistered client, aborting")
            return

        recall_group = self._recall_groups[osc_address]
        memory_slot = recall_group.memory_slots[osc_address]
        self._punch_piles[client_info.id].set_punch(recall_group, memory_slot, is_punch)
