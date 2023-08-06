from typing import Optional

from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.amount_ranges import T1AmountRanges, StrategyMaxBidRanges, StrategyMinBidRanges


class BidsRule(ValidationRule):
    def __init__(self, min_bid: Optional[float], max_bid: Optional[float]):
        self.min_bid = min_bid
        self.max_bid = max_bid

    def execute(self):
        """
        rules:
        if both defined min <= max
        range:  0.01 - 9,999,999.99
        """

        # ignore rule when no bids provided
        if self.min_bid is None and self.max_bid is None:
            return

        if self.min_bid > self.max_bid:
            raise ValidationException("min_bid must be less or equal to max_bid")

        T1AmountRanges(type_ranges=StrategyMinBidRanges,
                       amount=self.min_bid,
                       amount_field="min_bid").execute()

        T1AmountRanges(type_ranges=StrategyMaxBidRanges,
                       amount=self.max_bid,
                       amount_field="max_bid").execute()
