from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.input_type_required import InputTypeRequiredRule
from ts_t1_validator.models.enums.input_type import InputTypeEnum
from typing import Optional, Union


class InputTypeRequiredPutRule(ValidationRule):
    def __init__(self, pacing_amount: Optional[float],
                 impression_pacing_amount: Union[float, int, None], frequency_amount: Union[float, int, None],
                 min_bid: Optional[float], max_bid: Optional[float],
                 goal_value: Optional[float], roi_target: Optional[float],
                 input_type: InputTypeEnum):
        assert type(pacing_amount) is float or pacing_amount is None, "pacing_amount should be type float or None"
        assert type(min_bid) is float or min_bid is None, "min_bid should be type float or None"
        assert type(max_bid) is float or max_bid is None, "max_bid should be type float or None"
        assert type(goal_value) in [float, int] or goal_value is None, "goal_value should be type float or None"
        assert type(roi_target) is float or roi_target is None, "roi_target should be type float or None"

        self.pacing_amount = pacing_amount
        self.impression_pacing_amount = impression_pacing_amount
        self.frequency_amount = frequency_amount
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.goal_value = goal_value
        self.roi_target = roi_target
        self.input_type = input_type

    def execute(self):
        """
        rules:
            input_type is required if defined one of cap_amounts
        :return: None
        """

        required = [self.pacing_amount, self.impression_pacing_amount, self.frequency_amount,
                    self.min_bid, self.max_bid, self.goal_value, self.roi_target]

        if any([n is not None for n in required]):
            InputTypeRequiredRule(input_type=self.input_type).execute()
