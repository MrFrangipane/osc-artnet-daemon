import logging
from copy import copy

from oscartnetdaemon.components.mood_store.abstract import AbstractMoodStore
from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.osc_client_info import OSCClientInfo

_logger = logging.getLogger(__name__)


class _ClientMoodStore:
    def __init__(self, client_info: OSCClientInfo):
        self._client_info = client_info
        self._mood_store = {
            'before_temp': Mood(),
            'before_punch': Mood(),
            'a': Mood(),
            'b': Mood(),
            'c': Mood(),
            'd': Mood()
        }
        self._is_punching = False
        self._punch_pile: list[str] = ['before_punch']

    def save(self, scene_name):
        mood = copy(Components().osc_state_model.mood)
        self._mood_store[scene_name] = mood

    def recall(self, scene_name):
        mood = copy(self._mood_store[scene_name])
        self._set_mood(mood)

    def set_punch(self, scene_name, is_punch):
        if is_punch:
            if self._punch_pile == ['before_punch']:
                self._mood_store['before_punch'] = copy(Components().osc_state_model.mood)

            self._punch_pile.append(scene_name)
            self._set_mood(self._mood_store[scene_name])
        else:
            self._punch_pile.remove(scene_name)
            self._set_mood(self._mood_store[self._punch_pile[-1]])

    def set_temporary_modifier(self, is_temp_active):
        if is_temp_active:
            self._mood_store['before_temp'] = copy(Components().osc_state_model.mood)
        else:
            self._set_mood(self._mood_store['before_temp'])

    @staticmethod
    def _set_mood(mood: Mood):
        Components().osc_state_model.mood = copy(mood)
        Components().osc_message_sender.send_mood_to_all()


class MoodStore(AbstractMoodStore):
    def __init__(self):
        self._clients_stores: dict[str, _ClientMoodStore] = dict()

    def register_client(self, info: OSCClientInfo):
        _logger.debug(f"Registering client {info.name}")
        if info.name not in self._clients_stores:
            self._clients_stores[info.name] = _ClientMoodStore(info)

    def unregister_client(self, info: OSCClientInfo):
        pass  # keep data alive (for when client reconnects)

    def save(self, sender, scene_name):
        self._clients_stores[sender].save(scene_name)

    def recall(self, sender, scene_name):
        self._clients_stores[sender].recall(scene_name)

    def set_punch(self, sender, scene_name, is_punch):
        self._clients_stores[sender].set_punch(scene_name, is_punch)

    def set_temporary_modifier(self, sender, is_active):
        self._clients_stores[sender].set_temporary_modifier(is_active)
