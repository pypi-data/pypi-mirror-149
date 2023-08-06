from enum import unique
from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class CapTypeEnum(AbstractEnum):
    EVEN = "even"
    ASAP = "asap"
    NO_LIMIT = "no-limit"
    UNDEFINED = None

    @classmethod
    def list(cls) -> str:
        return ", ".join("'{0}'".format(x.value) for x in cls if x.value is not None)
