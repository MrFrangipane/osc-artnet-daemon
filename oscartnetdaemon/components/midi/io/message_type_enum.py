from enum import Enum


class MIDIMessageType(Enum):
    PitchWheel = 'pitchwheel'
    NoteOn = 'note_on'
    SysEx = 'sysex'
    ActiveSensing = 'active_sensing'
    ControlChange = 'control_change'
