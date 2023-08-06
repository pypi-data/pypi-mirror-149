from ts_t1_validator.models.enums.goal_type import GoalTypeEnum
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class StrategyGoalTypesForPGRule(ValidationRule):
    def __init__(self, goal_type: GoalTypeEnum):
        self.goal_type = goal_type

    def execute(self):
        """
        Case:
         For PG campaign the only type is 'spend'
        """
        if self.goal_type not in [GoalTypeEnum.SPEND]:
            raise ValidationException("'goal_type' must be 'spend' for Programmatic Guaranteed campaign")
