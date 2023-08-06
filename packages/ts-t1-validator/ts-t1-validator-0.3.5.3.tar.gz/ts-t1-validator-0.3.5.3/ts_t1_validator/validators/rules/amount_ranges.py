from .abstract_rule import ValidationRule
from enum import Enum

from ..exceptions import ValidationException


class CampaignRanges(Enum):
    FIXED_MIN_VALUE = 1.00
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class CampaignImpressionRanges(Enum):
    FIXED_MIN_VALUE = 1
    FIXED_MAX_VALUE = 9999999
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyFrequencyRanges(Enum):
    FIXED_MIN_VALUE = 1
    FIXED_MAX_VALUE = 9999999
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyImpressionRanges(Enum):
    FIXED_MIN_VALUE = 1
    FIXED_MAX_VALUE = 9999999
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyGoalRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyMaxBidRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyMinBidRanges(Enum):
    FIXED_MIN_VALUE = 0
    FIXED_MAX_VALUE = 9999999.99
    PERCENTAGE_MIN_VALUE = -99.99
    PERCENTAGE_MAX_VALUE = 9999999.99


class StrategyBudgetRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9_999_999.99


class StrategyRoiTargetRanges(Enum):
    FIXED_MIN_VALUE = 0.01
    FIXED_MAX_VALUE = 9_999_999.99


class T1AmountRanges(ValidationRule):
    def __init__(self, amount, type_ranges, amount_field):
        assert type(type_ranges) is Enum.__class__

        self.type_ranges = type_ranges
        self.amount = amount
        self.amount_field = amount_field

    def execute(self):
        """
        rules:
            valid range is 0.01 and 9999999.99
        """

        if self.amount is None or (not isinstance(self.amount, float) and not isinstance(self.amount, int)):
            raise ValidationException(f"{self.amount_field} must be numeric type")

        template = "value for {field_name} must be between " \
                   "{min_value:,.2f} and {max_value:,.2f}"
        if type(self.type_ranges.FIXED_MIN_VALUE.value) is int:
            template = "value for {field_name} must be between " \
                       "{min_value:,} and {max_value:,}"

        if not (self.type_ranges.FIXED_MIN_VALUE.value <= self.amount <= self.type_ranges.FIXED_MAX_VALUE.value):
            raise ValidationException(template.format(
                **{
                    "field_name": self.amount_field,
                    "min_value": self.type_ranges.FIXED_MIN_VALUE.value,
                    "max_value": self.type_ranges.FIXED_MAX_VALUE.value
                }))
