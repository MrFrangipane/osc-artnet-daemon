from oscartnetdaemon.core.components import Components

from oscartnetdaemon.components.midi_tempo.ableton_live import AbletonLiveMidiTempo
from oscartnetdaemon.components.midi_tempo.fallback_tap import FallbackTapMidiTempo


def inject_midi_tempo():
    configuration = Components().configuration
    implementations = (
        AbletonLiveMidiTempo,
        FallbackTapMidiTempo
    )

    for implementation in implementations:
        instance =  implementation()
        instance.set_in_port(configuration.midi_in_port)
        instance.set_out_port(configuration.midi_out_port)
        if instance.is_injectable():
            Components().midi_tempo = instance
            return

    if Components().midi_tempo is None:
        raise Exception("No MIDI tempo implementation found")
