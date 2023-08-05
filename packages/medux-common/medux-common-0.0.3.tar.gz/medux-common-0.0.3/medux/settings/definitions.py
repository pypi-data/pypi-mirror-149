from enum import Enum, IntEnum


class Scope(IntEnum):
    VENDOR = 1
    TENANT = 2
    GROUP = 3
    DEVICE = 4
    USER = 5


class ScopeIcons(Enum):
    VENDOR = "box2"  # -fill
    TENANT = "person-badge"  # -fill
    GROUP = "people"  # -fill
    DEVICE = "display"  # -fill
    USER = "person"  # -fill


class KeyType(Enum):
    BOOLEAN = "bool"
    STRING = "str"
    INTEGER = "int"
