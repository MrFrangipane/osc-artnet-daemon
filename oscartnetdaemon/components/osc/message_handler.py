import logging

from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.osc.state_model import OSCStateModel

_logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self):
        if Components().osc_message_sender is None:
            raise ValueError("No message sender is configured")

    def handle(self, address, values) -> None:
        try:
            path_items = address.split('/')
            value = values[0]

            if len(values) != 1:
                return

            if 'pager' in path_items:
                Components().osc_state_model.current_page = OSCStateModel.Page(values[0])
                return

            _, sender, control_name = path_items

            # fixme: we shouldn't know what to do here
            if sender.startswith('#two_bright_par'):
                par_index, value_name = control_name.split("_")
                par_index = int(par_index) - 1
                setattr(Components().osc_state_model.two_bright_par.pars[par_index], value_name, value)
                return

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

            #
            # Controls
            if control_name == "temporary_modifier":
                Components().mood_store.set_temporary_modifier(sender, value)

            if control_name == "tap_tempo" and value == 1:
                # fixme: specific OSC messages to notify other (messages get lost in timings)
                Components().midi_tempo.send_tap()

            elif control_name == 'recallable_dimmer':
                Components().osc_state_model.mood.recallable_dimmer = value
            elif control_name == 'master_dimmer':
                Components().osc_state_model.mood.master_dimmer = value

            elif control_name == 'hue':
                Components().osc_state_model.mood.hue = value
            elif control_name == 'texture':
                Components().osc_state_model.mood.texture = value

            elif control_name == 'bpm_scale':
                # fixme: we need an interop service between tosc and mood
                Components().osc_state_model.mood.bpm_scale = value
            elif control_name == 'palette':
                Components().osc_state_model.mood.palette = value
            elif control_name == 'pattern':
                Components().osc_state_model.mood.pattern = value

            elif control_name == 'pattern_parameter':
                Components().osc_state_model.mood.pattern_parameter = value
            elif control_name == 'pattern_playmode':
                Components().osc_state_model.mood.pattern_playmode = value

            elif control_name == 'on_octo':
                Components().osc_state_model.mood.on_octo = value
            elif control_name == 'on_lyre':
                Components().osc_state_model.mood.on_lyre = value
            elif control_name == 'on_wash':
                Components().osc_state_model.mood.on_wash = value
            elif control_name == 'on_par':
                Components().osc_state_model.mood.on_par = value
    #gouigoui 17/07/2024
            elif control_name == 'on_talk':
                Components().osc_state_model.mood.on_talk = value
            elif control_name == 'on_white':
                Components().osc_state_model.mood.on_white = value
            elif control_name == 'on_strobe':
                Components().osc_state_model.mood.on_strobe = value

            Components().osc_message_sender.send(control_name, value, sender)
        except Exception as e:
            _logger.warning(str(e))
