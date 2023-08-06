from ts_t1_validator.utils import is_number
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.frequency_type import FrequencyTypeRule
from ts_t1_validator.models.enums.frequency_interval import FrequencyIntervalEnum
from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum


class FrequencyTypePutRule(ValidationRule):
    def __init__(self, frequency_optimization: bool,
                 frequency_type: FrequencyTypeEnum,
                 frequency_amount,
                 frequency_interval: FrequencyIntervalEnum):

        assert type(frequency_type) is FrequencyTypeEnum, "frequency_type should be type of FrequencyTypeEnum"
        assert type(frequency_interval) is FrequencyIntervalEnum, \
            "frequency_interval should be type of FrequencyIntervalEnum"

        self.frequency_optimization = frequency_optimization
        self.frequency_type = frequency_type
        self.frequency_amount = frequency_amount
        self.frequency_interval = frequency_interval

    def put(self, frequency_type: FrequencyTypeEnum,
            frequency_interval: FrequencyIntervalEnum,
            frequency_amount: int or float or None):
        """
        :param frequency_type: FrequencyTypeEnum
        :param frequency_interval: FrequencyIntervalEnum
        :param frequency_amount: int or float or None
        :return: self
        """

        if self.frequency_optimization:
            self.frequency_amount = frequency_amount
            self.frequency_type = frequency_type
            self.frequency_interval = frequency_interval

        if self.frequency_type is FrequencyTypeEnum.NO_LIMIT:
            self.frequency_interval = frequency_interval
            self.frequency_amount = frequency_amount

        if is_number(frequency_amount):
            self.frequency_amount = frequency_amount

        return self

    def execute(self):
        """
        rule:
        frequency_optimization, frequency_type, frequency_amount, frequency_interval
            - if undefined in DB, follow POST logic
        """

        validator = FrequencyTypeRule(
            frequency_optimization=self.frequency_optimization,
            frequency_type=self.frequency_type,
            frequency_amount=self.frequency_amount,
            frequency_interval=self.frequency_interval)

        return validator.execute()
