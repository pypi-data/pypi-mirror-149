from ts_t1_validator.models.enums.goal_type import GoalTypeEnum
from ts_t1_validator.models.enums.input_type import InputTypeEnum
from ts_t1_validator.utils import is_int
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class GoalTypeRule(ValidationRule):
    def __init__(self, goal_type: GoalTypeEnum, goal_value):
        self.goal_type = goal_type
        self.goal_value = goal_value
        self.input_type = None
        self.percentage_min_value = 1
        self.percentage_max_value = 100
        self.fixed_min_value = 1
        self.fixed_max_value = 9999999.9999

    def execute(self):
        enum_message = "{0} must be one of [{1}]"

        # goal_type should be one of ctr, vcr, viewability_rate, cpa, cpc, reach, roi, spend, vcpm
        if self.goal_type is GoalTypeEnum.UNDEFINED:
            raise ValidationException(enum_message.format("goal_type", GoalTypeEnum.list()))

        # define type of amount value
        if self.goal_type.isPercentage():
            self.input_type = InputTypeEnum.PERCENTAGE
        else:
            self.input_type = InputTypeEnum.FIXED

        # goal_value should be int or float
        if not (isinstance(self.goal_value, float) or self.goal_value is None or isinstance(self.goal_value, int)):
            raise ValidationException("goal_value must be numeric type")

        # verify goal_value limits based on goal_type
        if self.goal_value is not None:
            if self.input_type is InputTypeEnum.PERCENTAGE:
                if not is_int(self.goal_value):
                    if self.goal_value - int(self.goal_value) > 0:
                        raise ValidationException("goal_value must be integer")
                if not (self.percentage_min_value <= self.goal_value <= self.percentage_max_value):
                    raise ValidationException(
                        "value for {field_name} when input_type=percentage must be between "
                        "{min_value:,.0f} and {max_value:,.0f}".format(
                            **{
                                "field_name": "goal_value",
                                "min_value": self.percentage_min_value,
                                "max_value": self.percentage_max_value
                            }))
            else:

                template = "value for {field_name} when input_type=fixed must be between " \
                           "{min_value:,.4f} and {max_value:,.4f}"
                if type(self.goal_value) is not float:
                    raise ValidationException("goal_value must be float")
                if not (self.fixed_min_value <= self.goal_value <= self.fixed_max_value):
                    raise ValidationException(template.format(**{
                        "field_name": "goal_value",
                        "min_value": self.fixed_min_value,
                        "max_value": self.fixed_max_value
                    }))
