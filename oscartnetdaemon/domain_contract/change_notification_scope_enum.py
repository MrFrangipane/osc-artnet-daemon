from enum import Enum


class ChangeNotificationScope(Enum):
    Broadcast = "Broadcast"
    Local = "Local"
    Foreign = "OnlyForeign"
