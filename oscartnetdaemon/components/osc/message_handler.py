from dataclasses import fields
from datetime import datetime
from typing import Union
import logging

from oscartnetdaemon.core.components import Components
from oscartnetdaemon.core.mood import Mood
from oscartnetdaemon.core.osc.state_model import OSCStateModel

_logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self):
        self._last_message_datetime: Union[datetime.date, None] = None
        if Components().osc_message_sender is None:
            raise ValueError("No message sender is configured")

        self._mood_attributes = [field.name for field in fields(Mood)]

    def handle(self, reply: tuple[str, int], address: str, *values) -> None:
        client_ip, client_port = reply
        _logger.debug(f"{client_ip}:{client_port} {address} {values}")
        self._last_message_datetime = datetime.now()

        try:
            Components().osc_message_sender.ensure_registered(client_ip, client_port)

            path_items = address.split('/')
            value = values[0]

            if len(values) != 1:
                return

            if 'pager' in path_items:
                Components().osc_state_model.current_page = OSCStateModel.Page(values[0])
                return

            _, page, control_name = path_items

            # fixme: we shouldn't know what to do here
            if page.startswith('#two_bright_par'):
                par_index, value_name = control_name.split("_")
                par_index = int(par_index) - 1
                setattr(Components().osc_state_model.two_bright_par.pars[par_index], value_name, value)
                return

            if page.startswith('#'):
                page_name = page[1:]
                setattr(getattr(Components().osc_state_model, page_name), control_name, value)
                return

            elif control_name.startswith('scene_'):
                _, scene_name, action = address.split('_')
                if action == "save" and value == 1:
                    Components().mood_store.save(client_ip, scene_name)

                if action == "recall" and value == 1:
                    Components().mood_store.recall(client_ip, scene_name)

                if action == "punch":
                    Components().mood_store.set_punch(client_ip, scene_name, value)
                    Components().osc_message_sender.notify_punch(client_ip, value)

                return

            #
            # Controls - specific
            if control_name == "temporary_modifier":
                Components().mood_store.set_temporary_modifier(client_ip, value)

            elif control_name == "tap_tempo" and value == 1:
                # fixme: specific OSC messages to notify other (messages get lost in timings)
                Components().midi_tempo.send_tap()

            elif control_name == "autoplay_on":
                Components().mood_store.set_autoplay(client_ip, value)

            #
            # Controls - all others
            elif control_name in self._mood_attributes:
                setattr(Components().osc_state_model.mood, control_name, value)

            Components().osc_message_sender.send(control_name, value, client_ip)

        except Exception as e:
            _logger.warning(str(e))
            raise
