import logging
from copy import copy

from oscartnetdaemon.components.mood_store.abstract import AbstractMoodStore
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.four_moods import FourMoods
from oscartnetdaemon.core.osc_client_info import OSCClientInfo

_logger = logging.getLogger(__name__)


# FIXME find better names for FourMoods and MoodStore
class MoodStore(AbstractMoodStore):
    def __init__(self):
        self._saved_moods: dict[str, FourMoods] = dict()

    def register_client(self, info: OSCClientInfo):
        _logger.info(f"Registering client {info.name}")
        self._saved_moods[info.name] = FourMoods()

    def unregister_client(self, info: OSCClientInfo):
        _logger.debug(f"Unregistering client {info.name}")
        self._saved_moods.pop(info.name)

    def save(self, sender, scene_name):
        _logger.debug(f"Saving scene {sender}/{scene_name}")
        # setattr(self._saved_moods[sender], "a", 8)
        mood = copy(Components().mood)
        print("save", mood)
        setattr(self._saved_moods[sender], scene_name, mood)

    def load(self, sender, scene_name):
        _logger.debug(f"Loading scene {sender}/{scene_name}")
        mood = copy(getattr(self._saved_moods[sender], scene_name))
        print("load", mood)
        Components().mood = mood
        Components().osc_message_sender.send_mood_to_all()

    def set_punch(self, sender, scene_name, is_punch):
        if is_punch:
            self.save(sender, self._before_punch)
            self.load(sender, scene_name)
        else:
            self.load(sender, self._before_punch)
