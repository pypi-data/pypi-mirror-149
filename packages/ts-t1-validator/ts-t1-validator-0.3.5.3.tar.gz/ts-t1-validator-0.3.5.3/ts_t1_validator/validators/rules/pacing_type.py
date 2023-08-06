from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.models.enums.pacing_interval import PacingIntervalEnum
from ts_t1_validator.models.enums.pacing_type import PacingTypeEnum


class PacingTypeRule(ValidationRule):
    def __init__(self, pacing_type: PacingTypeEnum, pacing_amount, pacing_interval: PacingIntervalEnum):
        self.pacing_type = pacing_type
        self.pacing_amount = pacing_amount
        self.pacing_interval = pacing_interval

    def execute(self):
        if self.pacing_type is not PacingTypeEnum.UNDEFINED:
            """
            rule:
                pacing_amount required if pacing_type is defined
                error message: "{:field_name} is required when pacing_type is defined"
            :return:
            """
            if self.pacing_amount is None:
                raise ValidationException("pacing_amount is required when pacing_type is defined")

            """
            rule:
                pacing_interval required if pacing_type is defined
                error message: "{:field_name} is required when pacing_type is defined"
            :return:
            """
            if self.pacing_interval is PacingIntervalEnum.UNDEFINED:
                raise ValidationException("pacing_interval is required when pacing_type is defined")
        else:
            if self.pacing_interval is not PacingIntervalEnum.UNDEFINED:
                raise ValidationException("pacing_type is required when pacing_interval is defined")

            if self.pacing_amount is not None:
                raise ValidationException("pacing_interval is required when pacing_amount is defined")
