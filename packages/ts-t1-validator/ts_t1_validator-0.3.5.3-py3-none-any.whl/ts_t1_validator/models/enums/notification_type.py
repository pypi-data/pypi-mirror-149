from enum import unique

from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class NotificationTypeEnum(AbstractEnum):
    CAMPAIGN = "campaign"
    ORGANIZATION = "organization"
    AGENCY = "agency"
    ADVERTISER = "advertiser"
    UNDEFINED = None
