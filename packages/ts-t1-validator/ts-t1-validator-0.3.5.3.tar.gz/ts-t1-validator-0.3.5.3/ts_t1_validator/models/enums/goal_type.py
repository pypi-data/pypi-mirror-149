from enum import unique

from ts_t1_validator.models.enums.abstract_enum import AbstractEnum


@unique
class PercentageGoalTypeEnum(AbstractEnum):
    CTR = "ctr"
    VCR = "vcr"
    VR = "viewability_rate"


@unique
class FixedGoalTypeEnum(AbstractEnum):
    CPA = "cpa"
    CPC = "cpc"
    REACH = "reach"
    ROI = "roi"
    SPEND = "spend"
    VCPM = "vcpm"


@unique
class GoalTypeEnum(AbstractEnum):
    CPA = "cpa"
    CPC = "cpc"
    REACH = "reach"
    ROI = "roi"
    SPEND = "spend"
    VCPM = "vcpm"
    CTR = "ctr"
    VCR = "vcr"
    VR = "viewability_rate"
    UNDEFINED = None

    def isFixed(self) -> bool:
        """
        check value in fixed list
        :return: bool
        """
        return self.value in FixedGoalTypeEnum.asList()

    def isPercentage(self) -> bool:
        """
        check value in percentage list
        :return: bool
        """
        return self.value in PercentageGoalTypeEnum.asList()

    @classmethod
    def list(cls) -> str:
        return ", ".join("'{0}'".format(x.value) for x in cls if x.value is not None)
