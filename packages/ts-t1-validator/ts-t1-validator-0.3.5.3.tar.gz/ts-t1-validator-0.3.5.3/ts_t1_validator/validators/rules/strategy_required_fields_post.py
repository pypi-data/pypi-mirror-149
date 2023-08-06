from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.models.enums.impression_pacing_type import ImpressionPacingTypeEnum
from ts_t1_validator.models.enums.pacing_type import PacingTypeEnum
from typing import Union, Optional


class StrategyPostRequiredFieldsRule(ValidationRule):
    def __init__(self,
                 pacing_type: PacingTypeEnum,
                 impression_pacing_type: ImpressionPacingTypeEnum,
                 min_bid: Union[float, int, None],
                 max_bid: Union[float, int, None],
                 goal_value: Union[float, int, None],
                 roi_target: Union[float, int, None],
                 frequency_optimization: Optional[bool]):

        self.pacing_type = pacing_type
        self.impression_pacing_type = impression_pacing_type
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.goal_value = goal_value
        self.roi_target = roi_target
        self.frequency_optimization = frequency_optimization

    def execute(self):
        """
        rules:
            at least one of the following is required: pacing_type, impression_pacing_type,
            min_bid, max_bid, goal_value, frequency_optimization,
            roi_target
        :return:
        """

        if self.pacing_type is not PacingTypeEnum.UNDEFINED:
            return

        if self.impression_pacing_type is not ImpressionPacingTypeEnum.UNDEFINED:
            return

        if self.min_bid is not None:
            return

        if self.max_bid is not None:
            return

        if self.goal_value is not None:
            return

        if self.roi_target is not None:
            return

        if self.frequency_optimization is not None:
            return

        raise ValidationException("At least one of the following is required: pacing_type, impression_pacing_type, min_bid, max_bid, goal_value, roi_target, frequency_optimization")
