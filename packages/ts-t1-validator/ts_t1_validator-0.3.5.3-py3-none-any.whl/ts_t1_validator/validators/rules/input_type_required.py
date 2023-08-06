from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.models.enums.input_type import InputTypeEnum


class InputTypeRequiredRule(ValidationRule):
    def __init__(self, input_type: InputTypeEnum):
        assert type(input_type) is InputTypeEnum, "input_type should be type of InputTypeEnum"

        self.input_type = input_type

    def execute(self):
        """
        rules:
            input_type is required for all post requests we have
        :return: None
        """
        if self.input_type is InputTypeEnum.UNDEFINED:
            raise ValidationException("input_type value must be one of the following values ('%s')" % "','".join([InputTypeEnum.FIXED.value, InputTypeEnum.PERCENTAGE.value]))
