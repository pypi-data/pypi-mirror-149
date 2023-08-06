from .abstract_rule import ValidationRule
from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum
from ts_t1_validator.models.enums.frequency_interval import FrequencyIntervalEnum
from ts_t1_validator.validators.rules.frequency_required_fields import FrequencyRequiredFieldsRule


class FrequencyRequiredFieldsPutRule(ValidationRule):
    def __init__(self, frequency_type, frequency_optimization, frequency_interval, frequency_amount, cap_fields={}):
        assert isinstance(frequency_type, FrequencyTypeEnum), "frequency_type should be type of FrequencyTypeEnum"
        assert isinstance(frequency_optimization, bool) or frequency_optimization is None, \
            "frequency_optimization should be type of bool or None"
        assert isinstance(frequency_interval, FrequencyIntervalEnum), \
            "frequency_interval should be type of FrequencyIntervalEnum"

        self.frequency_type = frequency_type
        self.frequency_optimization = frequency_optimization
        self.frequency_amount = frequency_amount
        self.frequency_interval = frequency_interval
        self.cap_fields = cap_fields

    def put(self, frequency_amount: float or None, frequency_interval: FrequencyIntervalEnum, frequency_type: FrequencyTypeEnum):
        """
        method to reset fields in case we update the model, there is the only case:
        1) user switches type to no-limit, in this case both, amount and interval should be switched to None

        :param frequency_amount: float or None
        :param frequency_interval: FrequencyIntervalEnum
        :param frequency_type: FrequencyTypeEnum
        :return: self
        """

        if self.frequency_type is FrequencyTypeEnum.NO_LIMIT:
            self.frequency_interval = frequency_interval
            self.frequency_amount = frequency_amount

        if self.frequency_optimization:
            self.frequency_interval = frequency_interval
            self.frequency_amount = frequency_amount
            self.frequency_type = frequency_type

        return self

    def execute(self):
        """
        rule:
        common logic should stay the same
        """

        postValidator = (FrequencyRequiredFieldsRule(frequency_type=self.frequency_type, frequency_optimization=self.frequency_optimization,
                                                     frequency_interval=self.frequency_interval, frequency_amount=self.frequency_amount,
                                                     cap_fields={"frequency_optimization": "frequency_optimization",
                                                                 "frequency_type": "frequency_type",
                                                                 "frequency_amount": "frequency_amount",
                                                                 "frequency_interval": "frequency_interval"}))

        return postValidator.execute()
