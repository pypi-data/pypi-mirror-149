from enum import Enum


class AbstractEnum(Enum):
    @classmethod
    def set(cls, value):
        return cls(value) if any(value == item.value for item in cls) else cls(None)

    @classmethod
    def asList(cls) -> list:
        """
        Present enum values in list format
        :return: list
        """
        return [x.value for x in list(cls) if x.value is not None]
