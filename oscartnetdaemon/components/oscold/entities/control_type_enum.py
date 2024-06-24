from enum import Enum


class OSCControlType(Enum):
    Button = 'Button'
    ColorWheel = 'ColorWheel'
    Fader = 'Fader'
    Radio = 'Radio'
    RecallSlot = 'RecallSlot'
    Toggle = 'Toggle'
