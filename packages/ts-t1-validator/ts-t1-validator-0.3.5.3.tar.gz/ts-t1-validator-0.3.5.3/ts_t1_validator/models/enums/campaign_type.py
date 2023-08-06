from enum import unique
from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class CampaignTypeEnum(AbstractEnum):
    PMP = "PMP"
    PG = "PG"
    UNDEFINED = None
