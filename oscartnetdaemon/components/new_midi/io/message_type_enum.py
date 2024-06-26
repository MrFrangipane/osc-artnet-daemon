from enum import Enum


class MIDIMessageType(Enum):
    PitchWheel = 'pitchwheel'
    NoteOn = 'note_on'
