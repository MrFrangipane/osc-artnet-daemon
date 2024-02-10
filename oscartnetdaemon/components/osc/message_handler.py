from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.osc.state_model import OSCStateModel


class MessageHandler:
    def __init__(self):
        if Components().osc_message_sender is None:
            raise ValueError("No message sender is configured")

    def handle(self, address, values) -> None:
        path_items = address.split('/')
        value = values[0]

        if len(values) != 1:
            return

        if 'pager' in path_items:
            Components().osc_state_model.current_page = OSCStateModel.Page(values[0])
            return

        _, sender, control_name = path_items

        if sender.startswith('#'):
            page_name = sender[1:]
            setattr(getattr(Components().osc_state_model, page_name), control_name, value)
            return

        elif control_name.startswith('scene_'):
            _, scene_name, action = address.split('_')
            if action == "save" and value == 1:
                Components().mood_store.save(sender, scene_name)

            if action == "recall" and value == 1:
                Components().mood_store.recall(sender, scene_name)

            if action == "punch":
                Components().mood_store.set_punch(sender, scene_name, value)
                Components().osc_message_sender.notify_punch(sender, value)

            return

        if control_name == 'palette':
            Components().osc_state_model.mood.palette = value
        elif control_name == 'animation':
            Components().osc_state_model.mood.animation = value
        elif control_name == 'texture':
            Components().osc_state_model.mood.texture = value
        elif control_name == 'blinking':
            Components().osc_state_model.mood.blinking = value
        elif control_name == 'bpm_scale':
            Components().osc_state_model.mood.bpm_scale = value  # fixme: we need an interop service between tosc and mood
        elif control_name == 'palette_animation':
            Components().osc_state_model.mood.palette_animation = value   # fixme: we need an interop service between tosc and mood

        Components().osc_message_sender.send(control_name, value, sender)
