from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ...models.enums.cap_type import CapTypeEnum
from ...models.enums.frequency_interval import FrequencyIntervalEnum
from ...models.enums.frequency_type import FrequencyTypeEnum


class ProgrammaticGuaranteedOverridesRule(ValidationRule):
    def __init__(self, spend_cap_type, spend_cap_automatic, spend_cap_amount, frequency_optimization,
                 frequency_type, frequency_interval, frequency_amount, restrict_targeting_to_same_device_id
                 ):
        assert type(spend_cap_type) is CapTypeEnum, "spend_cap_type should be CapTypeEnum type"
        assert type(frequency_type) is FrequencyTypeEnum, "frequency_type should be FrequencyTypeEnum type"
        assert type(frequency_interval) is FrequencyIntervalEnum, \
            "frequency_interval should be FrequencyIntervalEnum type"

        self.spend_cap_type = spend_cap_type
        self.spend_cap_automatic = spend_cap_automatic
        self.spend_cap_amount = spend_cap_amount
        self.frequency_optimization = frequency_optimization
        self.frequency_type = frequency_type
        self.frequency_interval = frequency_interval
        self.frequency_amount = frequency_amount
        self.restrict_targeting_to_same_device_id = restrict_targeting_to_same_device_id

    def execute(self):
        """
        rules:
            spend_cap_type must be 'no-limit'
            spend_cap_automatic must be 'off'
            spend_cap_amount must not be provided
            frequency_optimization must be 'off'
            frequency_type must be 'no-limit'
            frequency_interval must be not-applicable
            frequency_amount must not be provided
            restrict_targeting_to_same_device_id must be 'off'

            :return:
        """
        when_pg_message = "%s when campaign type is PG"
        if self.spend_cap_type != CapTypeEnum.NO_LIMIT:
            raise ValidationException(when_pg_message % "spend_cap_type must be 'no-limit'")

        if self.spend_cap_automatic is not False:
            raise ValidationException(when_pg_message % "spend_cap_automatic must be 'off'")

        if self.spend_cap_amount is not None:
            raise ValidationException(when_pg_message % "spend_cap_amount must not be provided")

        if self.frequency_optimization != 0:
            raise ValidationException(when_pg_message % "frequency_optimization must be 'off'")

        if self.frequency_type != FrequencyTypeEnum.NO_LIMIT:
            raise ValidationException(when_pg_message % "frequency_type must be 'no-limit'")

        if self.frequency_interval != FrequencyIntervalEnum.NOTAPPLICABLE:
            raise ValidationException(when_pg_message % " frequency_interval must be not-applicable")

        if self.frequency_amount is not None:
            raise ValidationException(when_pg_message % "frequency_amount must not be provided")

        if self.restrict_targeting_to_same_device_id != 0:
            raise ValidationException(when_pg_message % "restrict_targeting_to_same_device_id must be 'off'")
