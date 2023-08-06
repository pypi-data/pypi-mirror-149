from enum import unique

from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class InputTypeEnum(AbstractEnum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"
    UNDEFINED = None
