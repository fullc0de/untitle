from enum import Enum

class AttendeeType(str, Enum):
    user = "user"
    bot = "bot"