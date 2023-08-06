from enum import Enum, unique


@unique
class SwitcherEnum(Enum):
    ON = "on"
    OFF = "off"
    UNDEFINED = None

    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)

    @classmethod
    def fromBool(cls, value):
        if type(value) is bool:
            return cls.set((SwitcherEnum.OFF.value, SwitcherEnum.ON.value)[value])

        return cls.set(value)
