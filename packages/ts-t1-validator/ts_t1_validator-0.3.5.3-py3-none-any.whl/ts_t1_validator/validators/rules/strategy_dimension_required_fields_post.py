from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.models.enums.dimension_action import DimensionActionEnum
from ts_t1_validator.models.enums.dimension_code import DimensionCodeEnum


class StrategyDimensionPostRequiredFieldsRule(ValidationRule):
    def __init__(self, dimension_code, action, include_value_ids, exclude_value_ids):

        assert type(dimension_code) is DimensionCodeEnum, "dimension_code should be DimensionCodeEnum type"
        assert type(action) is DimensionActionEnum, "action should be DimensionActionEnum type"

        self.dimension_code = dimension_code
        self.action = action
        self.include_value_ids = include_value_ids
        self.exclude_value_ids = exclude_value_ids

    def execute(self):
        """
        rules:
        - action, dimension_code, include_value_ids or exclude_value_ids are required
        """
        if self.dimension_code is DimensionCodeEnum.UNDEFINED:
            raise ValidationException("dimension_code must be defined in the request")
        if self.action is DimensionActionEnum.UNDEFINED:
            raise ValidationException("action must be defined in the request")

        if self.include_value_ids is None and self.exclude_value_ids is None:
            raise ValidationException("at least one of include_value_ids or exclude_value_ids must be defined")
