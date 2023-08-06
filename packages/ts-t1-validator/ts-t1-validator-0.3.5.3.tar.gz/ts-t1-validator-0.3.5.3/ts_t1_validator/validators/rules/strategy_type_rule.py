from ts_t1_validator.models.enums.strategy_type import StrategyTypeEnum
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class StrategyTypeRule(ValidationRule):
    def __init__(self, strategy_type: StrategyTypeEnum):
        self.strategy_type = strategy_type

    def execute(self):
        """
        strategy_type should be kind of valid enumeration
        """

        if self.strategy_type is StrategyTypeEnum.UNDEFINED:
            raise ValidationException("strategy_type must be one of " + str(StrategyTypeEnum.asList()))
