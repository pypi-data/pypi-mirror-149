from enum import unique

from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class ImpressionPacingIntervalEnum(AbstractEnum):
    HOUR = "hour"
    DAY = "day"
    UNDEFINED = None
