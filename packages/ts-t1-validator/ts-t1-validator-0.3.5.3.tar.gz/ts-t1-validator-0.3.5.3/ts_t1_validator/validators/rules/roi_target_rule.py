from typing import Optional, Union

from ts_t1_validator.models.enums.goal_type import GoalTypeEnum
from ts_t1_validator.utils import is_number
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.amount_ranges import StrategyRoiTargetRanges, T1AmountRanges


class StrategyRoiTargetRule(ValidationRule):
    def __init__(self, goal_type: GoalTypeEnum, roi_target: Optional[Union[float, int]]):
        self.goal_type = goal_type
        self.roi_target = roi_target

    def execute(self):
        """
        In case 'goal_type' == 'roi' the validation rules are:
        - Become required
        - Should be in range from 0.01 to 9999999.99
        """

        if self.goal_type is GoalTypeEnum.ROI and self.roi_target is None:
            raise ValidationException("roi_target is mandatory when goal_type is 'roi'")

        if self.roi_target is None:
            return

        if not is_number(self.roi_target):
            raise ValidationException("roi_target must be a number")

        T1AmountRanges(type_ranges=StrategyRoiTargetRanges,
                       amount=self.roi_target,
                       amount_field="roi_target").execute()
