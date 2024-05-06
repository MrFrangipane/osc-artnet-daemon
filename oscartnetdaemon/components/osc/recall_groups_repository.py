import logging

from oscartnetdaemon.components.osc.abstract_recall_groups_repository import AbstractOSCRecallGroupsRepository
from oscartnetdaemon.components.osc.recall_group import OSCRecallGroup
from oscartnetdaemon.entities.osc.recall_group_info import OSCRecallGroupInfo
from oscartnetdaemon.components.osc.widgets.abstract import OSCAbstractWidget

_logger = logging.getLogger(__name__)


class OSCRecallGroupsRepository(AbstractOSCRecallGroupsRepository):

    def __init__(self):
        self._recall_groups: dict[str, OSCRecallGroup] = dict()

    def create_groups(self, widgets: list[OSCAbstractWidget], recall_group_infos: list[OSCRecallGroupInfo]):
        self._recall_groups = dict()
        widget_indexed: dict[str: OSCAbstractWidget] = {widget.info.name: widget for widget in widgets}

        for group_info in recall_group_infos:
            new_recall_group = OSCRecallGroup(
                name=group_info.name,
                widgets=[widget_indexed[name] for name in group_info.widget_names]
            )
            for widget_name in group_info.widget_names:
                self._recall_groups[widget_name] = new_recall_group

    def save_for_slot(self, slot_name: str):
        recall_group = self._recall_groups[slot_name]
        for widget in recall_group.widgets:
            recall_group.values[widget.info.name] = widget.get_values()

    def recall_for_slot(self, slot_name: str):
        # fixme: needs a memory per slot !!
        recall_group = self._recall_groups[slot_name]
        for widget in recall_group.widgets:
            widget.set_values(recall_group.values[widget.info.name])

    def set_punch_for_slot(self, slot_name: str, is_punch: bool):
        _logger.info(f"punch {slot_name} {is_punch}")
