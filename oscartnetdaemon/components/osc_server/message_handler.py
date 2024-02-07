from typing import Any

from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.mood import Mood


class MessageHandler:
    def __init__(self):
        self._mood: Mood = Components().mood

    def handle(self, address, values) -> [str, Any]:
        r_address, r_value = None, None

        if address == '/mood/palette':
            self._mood.palette = values[0]
        elif address == '/animation':
            self._mood.animation = values[0]
        elif address == '/texture':
            self._mood.texture = values[0]
        elif address == '/blinking':
            self._mood.blinking = values[0]
        elif address == '/mood/bpm_scale':
            self._mood.bpm_scale = [0.25, 0.5, 1, 2, 4][values[0]]
        elif address == '/mood/palette_animation':
            self._mood.palette_animation = [0.25, 0.5, 1, 2, 4][values[0]]

        elif address.startswith('/mood/scene_') and values[0] == 1:
            _, scene, action = address.split('_')
            print(scene, action)
            r_address, r_value = '/mood/palette_animation', 4

        return r_address, r_value
