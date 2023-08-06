from typing import Optional, Union

from ts_t1_validator.models.enums.impression_pacing_interval import ImpressionPacingIntervalEnum
from ts_t1_validator.utils import is_number, is_int
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.models.enums.impression_pacing_type import ImpressionPacingTypeEnum
from ts_t1_validator.models.enums.pacing_interval import PacingIntervalEnum


class ImpressionPacingTypeRule(ValidationRule):
    def __init__(self,
                 impression_pacing_type: ImpressionPacingTypeEnum,
                 impression_pacing_amount: Optional[Union[int, float]],
                 impression_pacing_interval: PacingIntervalEnum):
        self.impression_pacing_type = impression_pacing_type
        self.impression_pacing_amount = impression_pacing_amount
        self.impression_pacing_interval = impression_pacing_interval

    def execute(self):
        if self.impression_pacing_type is not ImpressionPacingTypeEnum.UNDEFINED:
            """
            rule:
                impression_pacing_amount required if impression_pacing_type is asap or even
                    - error message "{:field_name} is required when impression_pacing_type is asap or even"
                must be undefined if impression_pacing_type is no-limit
                    - error message "{:field_name} cannot be defined when impression_pacing_type is no-limit"
            """
            if self.impression_pacing_type in [ImpressionPacingTypeEnum.ASAP,
                                               ImpressionPacingTypeEnum.EVEN] and self.impression_pacing_amount is None:
                raise ValidationException("impression_pacing_amount is required when impression_pacing_type is asap or even")
            elif self.impression_pacing_type is ImpressionPacingTypeEnum.NO_LIMIT and self.impression_pacing_amount is not None:
                raise ValidationException("impression_pacing_amount cannot be defined when impression_pacing_type is no-limit")

            """
            rule:
                impression_pacing_interval required if impression_pacing_type is asap or even
                    - error message "{:field_name} is required when impression_pacing_type is asap or even"
                must be undefined if impression_pacing_type is no-limit
                    - error message "{:field_name} cannot be defined when impression_pacing_type is no-limit
            """
            if self.impression_pacing_type in [ImpressionPacingTypeEnum.ASAP,
                                               ImpressionPacingTypeEnum.EVEN] and self.impression_pacing_interval is PacingIntervalEnum.UNDEFINED:
                raise ValidationException("impression_pacing_interval is required when impression_pacing_type is asap or even")
            elif self.impression_pacing_type is ImpressionPacingTypeEnum.NO_LIMIT and self.impression_pacing_interval is not PacingIntervalEnum.UNDEFINED:
                raise ValidationException("impression_pacing_interval cannot be defined when impression_pacing_type is no-limit")

            """
            rule: for impression_pacing_amount, while input_type='fixed', type must be int
            rule: for impression_pacing_amount, while input_type='percentage', type must be float
            """
            if self.impression_pacing_type in [ImpressionPacingTypeEnum.ASAP,
                                               ImpressionPacingTypeEnum.EVEN]:
                if not is_number(self.impression_pacing_amount):
                    raise ValidationException("impression_pacing_amount must be a float")
        else:
            if self.impression_pacing_interval is not ImpressionPacingIntervalEnum.UNDEFINED:
                raise ValidationException("impression_pacing_type is required when impression_pacing_interval is defined")
            if self.impression_pacing_amount is not None:
                raise ValidationException("impression_pacing_interval is required when impression_pacing_amount is defined")
