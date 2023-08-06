from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class StrategyUseOptimizationForPGRule(ValidationRule):
    def __init__(self, use_optimization: bool):
        self.use_optimization = use_optimization

    def execute(self):
        """
        Case:
        For PG campaign use_optimization must be False
        """
        if self.use_optimization is True:
            raise ValidationException("'use_optimization' must be False for Programmatic Guaranteed campaign")
