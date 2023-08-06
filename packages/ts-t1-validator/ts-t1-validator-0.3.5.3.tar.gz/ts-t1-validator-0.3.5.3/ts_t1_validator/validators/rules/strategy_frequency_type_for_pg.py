from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class StrategyFrequencyTypeForPGRule(ValidationRule):
    def __init__(self, frequency_type: FrequencyTypeEnum):
        self.frequency_type = frequency_type

    def execute(self):
        """
        Case:
        For PG campaign frequency_type must be the only 'no-limit'
        """
        if self.frequency_type is not FrequencyTypeEnum.NO_LIMIT:
            raise ValidationException("'frequency_type' must be 'no-limit' for Programmatic Guaranteed campaign")
