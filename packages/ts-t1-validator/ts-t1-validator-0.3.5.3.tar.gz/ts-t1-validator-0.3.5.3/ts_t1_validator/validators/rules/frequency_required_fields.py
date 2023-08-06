from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum
from ts_t1_validator.models.enums.frequency_interval import FrequencyIntervalEnum


class FrequencyRequiredFieldsRule(ValidationRule):
    def __init__(self, frequency_type: FrequencyTypeEnum, frequency_optimization: bool,
                 frequency_interval: FrequencyIntervalEnum, frequency_amount, cap_fields=dict):
        self.frequency_type = frequency_type
        self.frequency_optimization = frequency_optimization
        self.frequency_amount = frequency_amount
        self.frequency_interval = frequency_interval
        self.cap_fields = cap_fields

    def execute(self):

        if self.frequency_interval is not FrequencyIntervalEnum.UNDEFINED and self.frequency_type is FrequencyTypeEnum.UNDEFINED:
            raise ValidationException(
                "If you define %(frequency_interval)s, you must define %(frequency_type)s" % self.cap_fields)

        if self.frequency_amount is not None and self.frequency_type is FrequencyTypeEnum.UNDEFINED:
            raise ValidationException(
                "If you define %(frequency_amount)s you must define %(frequency_type)s" % self.cap_fields)
