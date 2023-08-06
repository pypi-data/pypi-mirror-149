from enum import unique

from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class MediaTypeEnum(AbstractEnum):
    DISPLAY = "display"
    VIDEO = "video"
    UNDEFINED = None
