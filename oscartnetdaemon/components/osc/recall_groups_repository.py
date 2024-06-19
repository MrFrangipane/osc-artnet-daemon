import logging

from oscartnetdaemon.components.osc.abstract_recall_groups_repository import AbstractOSCRecallGroupsRepository
from oscartnetdaemon.components.osc.recall_group import OSCRecallGroup, OSCMemorySlot
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget

from oscartnetdaemon.entities.osc.client_info import OSCClientInfo
from oscartnetdaemon.entities.osc.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.entities.osc.widget_type_enum import OSCWidgetTypeEnum


_logger = logging.getLogger(__name__)


# fixme: move work to OSCRecallGroup objects ?
class OSCRecallGroupsRepository(AbstractOSCRecallGroupsRepository):

    def __init__(self):
        self._recall_groups: dict[str, OSCRecallGroup] = dict()
        self._punch_piles = None

    def create_groups(self, widgets: list[OSCAbstractWidget], recall_group_infos: list[OSCRecallGroupInfo]):
        self._recall_groups = dict()
        all_widgets_indexed: dict[str: OSCAbstractWidget] = {widget.info.osc_address: widget for widget in widgets}
        assigned_memory_slots_addresses: list[str] = list()

        for group_info in recall_group_infos:
            group_widgets = [
                all_widgets_indexed[osc_address]
                for osc_address in group_info.widget_osc_addresses
                if not all_widgets_indexed[osc_address].info.type == OSCWidgetTypeEnum.RecallSlot
            ]

            memory_slots: {str: OSCMemorySlot} = dict()
            for osc_address in group_info.widget_osc_addresses:
                if all_widgets_indexed[osc_address].info.type != OSCWidgetTypeEnum.RecallSlot:
                    continue

                if osc_address in assigned_memory_slots_addresses:
                    raise ValueError(f"Memory slot '{osc_address}' already in use in a Recall Group")

                memory_slots[osc_address] = OSCMemorySlot(osc_address=osc_address)
                assigned_memory_slots_addresses.append(osc_address)

            new_recall_group = OSCRecallGroup(
                name=group_info.name,
                widgets=group_widgets,
                memory_slots=memory_slots
            )

            for osc_address in memory_slots:
                self._recall_groups[osc_address] = new_recall_group

    def register_client(self, client_info: OSCClientInfo):
        pass

    def unregister_client(self, client_info: OSCClientInfo):
        pass

    def save_for_slot(self, osc_address: str):
        recall_group = self._recall_groups[osc_address]
        for widget in recall_group.widgets:
            recall_group.memory_slots[osc_address].widgets_values[widget.info.osc_address] = widget.get_values()

    def recall_for_slot(self, osc_address: str):
        recall_group = self._recall_groups[osc_address]
        for widget in recall_group.widgets:
            values = recall_group.memory_slots[osc_address].widgets_values.get(widget.info.osc_address, None)
            if values is not None:
                widget.set_values(values)

    def set_punch_for_slot(self, client_info: OSCClientInfo, osc_address: str, is_punch: bool):
        recall_group = self._recall_groups[osc_address]
        self._punch_piles[client_info.id].set_punch(recall_group.name, is_punch)
        _logger.info(f"punch {client_info} {osc_address} {is_punch}")
