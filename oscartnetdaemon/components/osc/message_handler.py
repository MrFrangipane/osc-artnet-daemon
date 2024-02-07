from oscartnetdaemon.core.components import Components


class MessageHandler:
    def __init__(self):
        if Components().osc_message_sender is None:
            raise ValueError("No message sender is configured")

    def handle(self, address, values) -> None:
        path_items = address.split('/')

        if 'pager' in path_items or len(values) != 1:
            return

        value = values[0]
        _, sender, control_name = path_items

        if control_name.startswith('scene_'):
            _, scene_name, action = address.split('_')
            if action == "save" and value == 1:
                Components().mood_store.save(sender, scene_name)

            if action == "recall" and value == 1:
                Components().mood_store.load(sender, scene_name)

            if action == "punch":
                Components().mood_store.set_punch(sender, scene_name, value)
                Components().osc_message_sender.notify_punch(sender, value)

            return

        if control_name == 'palette':
            Components().mood.palette = value
        elif control_name == 'animation':
            Components().mood.animation = value
        elif control_name == 'texture':
            Components().mood.texture = value
        elif control_name == 'blinking':
            Components().mood.blinking = value
        elif control_name == 'bpm_scale':
            Components().mood.bpm_scale = value  # fixme: we need an interop service between tosc and mood
        elif control_name == 'palette_animation':
            Components().mood.palette_animation = value   # fixme: we need an interop service between tosc and mood

        Components().osc_message_sender.send(control_name, value, sender)
