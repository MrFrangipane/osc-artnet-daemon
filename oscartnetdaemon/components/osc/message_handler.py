from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.mood import Mood


class MessageHandler:
    def __init__(self):
        self._mood: Mood = Components().mood
        self._message_sender = Components().osc_message_sender

        if self._message_sender is None:
            raise ValueError("No message sender is configured")

    def handle(self, address, values) -> None:
        path_items = address.split('/')

        if 'pager' in path_items or len(values) != 1:
            return

        value = values[0]
        _, sender, control_name = path_items

        if control_name.startswith('scene_') and value == 1:
            _, scene, action = address.split('_')
            return

        if control_name == 'palette':
            self._mood.palette = value
        elif control_name == 'animation':
            self._mood.animation = value
        elif control_name == 'texture':
            self._mood.texture = value
        elif control_name == 'blinking':
            self._mood.blinking = value
        elif control_name == 'bpm_scale':
            self._mood.bpm_scale = [0.25, 0.5, 1, 2, 4][value]
        elif control_name == 'palette_animation':
            self._mood.palette_animation = [0.25, 0.5, 1, 2, 4][value]

        self._message_sender.send(control_name, value, sender)
