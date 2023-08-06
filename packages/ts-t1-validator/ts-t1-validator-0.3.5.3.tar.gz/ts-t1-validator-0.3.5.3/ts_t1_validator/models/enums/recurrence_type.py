from enum import unique

from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class RecurrenceTypeEnum(AbstractEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    UNDEFINED = None
