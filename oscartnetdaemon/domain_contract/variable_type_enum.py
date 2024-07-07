from enum import Enum


class VariableType(Enum):
    Text = "Text"
    Fader = "Fader"
    Button = "Button"
    RecallSlot = 'RecallSlot'
    Indicator = "Indicator"
