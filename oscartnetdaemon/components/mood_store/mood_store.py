import logging
from copy import copy
from ipaddress import IPv4Address

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
            'd': Mood(),
            'e': Mood()
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
            if scene_name in self._punch_pile:
                self._punch_pile.remove(scene_name)
                self._set_mood(self._mood_store[self._punch_pile[-1]])

    def set_temporary_modifier(self, is_temp_active):
        if is_temp_active:
            self._mood_store['before_temp'] = copy(Components().osc_state_model.mood)
        else:
            self._set_mood(self._mood_store['before_temp'])

    def set_autoplay(self, is_autoplay):
        osc_state_model = Components().osc_state_model
        osc_state_model.mood.autoplay_on = is_autoplay
        if not is_autoplay:
            osc_state_model.autoplay_current_scene = -1
            osc_state_model.autoplay_lastest_client = ""
        osc_state_model.autoplay_lastest_client = '.'.join(str(int(b)) for b in self._client_info.address)
        mood = copy(Components().osc_state_model.mood)
        self._set_mood(mood)

    @staticmethod
    def _set_mood(mood: Mood):
        master = Components().osc_state_model.mood.master_dimmer
        autoplay_on = Components().osc_state_model.mood.autoplay_on
        autoplay_interval = Components().osc_state_model.mood.autoplay_interval

        mood.master_dimmer = master
        mood.autoplay_on = autoplay_on
        mood.autoplay_interval = autoplay_interval
        mood.autoplay_current = Components().osc_state_model.autoplay_current_scene

        Components().osc_state_model.mood = copy(mood)
        Components().osc_message_sender.send_mood_to_all()


class MoodStore(AbstractMoodStore):
    def __init__(self):
        # TODO : dont register clients in two places (MoodStore + MessageSender)
        self._clients_stores: dict[str, _ClientMoodStore] = dict()

    def register_client(self, info: OSCClientInfo):
        ip_address = str(IPv4Address(info.address))
        if ip_address not in self._clients_stores:
            self._clients_stores[ip_address] = _ClientMoodStore(info)

    def unregister_client(self, info: OSCClientInfo):
        pass  # keep data alive (for when client reconnects)

    def save(self, sender_ip, scene_name):
        self._clients_stores[sender_ip].save(scene_name)

    def recall(self, sender_ip, scene_name):
        self._clients_stores[sender_ip].recall(scene_name)

    def set_punch(self, sender_ip, scene_name, is_punch):
        self._clients_stores[sender_ip].set_punch(scene_name, is_punch)

    def set_temporary_modifier(self, sender_ip, is_active):
        self._clients_stores[sender_ip].set_temporary_modifier(is_active)

    def set_autoplay(self, sender_ip, is_autoplay):
        self._clients_stores[sender_ip].set_autoplay(is_autoplay)
