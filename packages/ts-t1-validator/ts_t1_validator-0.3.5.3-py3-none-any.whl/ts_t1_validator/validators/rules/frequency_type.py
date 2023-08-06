from ts_t1_validator.utils import is_number
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.models.enums.frequency_interval import FrequencyIntervalEnum
from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum


class FrequencyTypeRule(ValidationRule):
    def __init__(self,
                 frequency_optimization,
                 frequency_type: FrequencyTypeEnum,
                 frequency_amount,
                 frequency_interval: FrequencyIntervalEnum):
        self.frequency_optimization = frequency_optimization
        self.frequency_type = frequency_type
        self.frequency_amount = frequency_amount
        self.frequency_interval = frequency_interval

    def execute(self):
        if self.frequency_optimization is None:
            if self.frequency_type is not FrequencyTypeEnum.UNDEFINED:
                raise ValidationException("frequency_optimization is required when frequency_type is defined")

            if self.frequency_interval is not FrequencyIntervalEnum.UNDEFINED:
                raise ValidationException("frequency_optimization is required when frequency_interval is defined")

            if self.frequency_amount is not None:
                raise ValidationException("frequency_optimization is required when frequency_amount is defined")

            return

        """
            rules for 'frequency_type':
            required if frequency_optimization is FALSE
                - error message: "{:field_name} is required when frequency_optimization is FALSE"
            must be undefined if frequency_optimization is TRUE
                - error message: "{:field_name} cannot be defined when frequency_optimization is TRUE"
        """
        if self.frequency_optimization is False and self.frequency_type is FrequencyTypeEnum.UNDEFINED:
            raise ValidationException("frequency_type is required when frequency_optimization is 'off'")
        elif self.frequency_optimization is True and self.frequency_type is not FrequencyTypeEnum.UNDEFINED:
            raise ValidationException("frequency_type cannot be defined when frequency_optimization is 'on'")

        """
            rules for 'frequency_amount':
            required if frequency_type is asap or even
                - error message "{:field_name} is required when frequency_type is asap or even"
            must be undefined if frequency_optimization is TRUE
                - error message: "{:field_name} cannot be defined when frequency_optimization is TRUE"
            must be undefined if frequency_type is no-limit.
                - error message: "{:field_name} cannot be defined when frequency_type is no-limit"
        """
        if self.frequency_type in [FrequencyTypeEnum.ASAP, FrequencyTypeEnum.EVEN] and self.frequency_amount is None:
            raise ValidationException("frequency_amount is required when frequency_type is asap or even")
        elif self.frequency_optimization is True and self.frequency_amount is not None:
            raise ValidationException("frequency_amount cannot be defined when frequency_optimization is 'on'")
        elif self.frequency_type is FrequencyTypeEnum.NO_LIMIT and self.frequency_amount is not None:
            raise ValidationException("frequency_amount cannot be defined when frequency_type is no-limit")

        """
            rules for 'frequency_interval':
            required if frequency_type is asap or even
                - error message "{:field_name} is required when frequency_type is asap or even"
            must be undefined if frequency_optimization is TRUE
                - error message: "{:field_name} cannot be defined when frequency_optimization is TRUE"
            must be undefined if frequency_type is no-limit.
                - error message: "{:field_name} cannot be defined when frequency_type is no-limit"
        """
        if self.frequency_type in [FrequencyTypeEnum.ASAP,
                                   FrequencyTypeEnum.EVEN] and self.frequency_interval is FrequencyIntervalEnum.UNDEFINED:
            raise ValidationException("frequency_interval is required when frequency_type is asap or even")
        elif self.frequency_optimization is True and self.frequency_interval is not FrequencyIntervalEnum.UNDEFINED:
            raise ValidationException("frequency_interval cannot be defined when frequency_optimization is 'on'")
        elif self.frequency_type is FrequencyTypeEnum.NO_LIMIT and self.frequency_interval is not FrequencyIntervalEnum.UNDEFINED:
            raise ValidationException("frequency_interval cannot be defined when frequency_type is no-limit")

        if self.frequency_type in [FrequencyTypeEnum.ASAP,
                                   FrequencyTypeEnum.EVEN]:
            if not is_number(self.frequency_amount):
                raise ValidationException("frequency_amount must be a float")
