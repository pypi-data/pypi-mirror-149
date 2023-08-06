from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.pacing_type import PacingTypeRule
from ts_t1_validator.models.enums.pacing_interval import PacingIntervalEnum
from ts_t1_validator.models.enums.pacing_type import PacingTypeEnum


class PacingTypePutRule(ValidationRule):
    def __init__(self, pacing_type: PacingTypeEnum, pacing_amount: PacingIntervalEnum, pacing_interval):
        assert type(pacing_type) is PacingTypeEnum, "pacing_type should be PacingTypeEnum type"
        assert type(pacing_interval) is PacingIntervalEnum, "pacing_interval should be PacingIntervalEnum type"

        self.pacing_type = pacing_type
        self.pacing_amount = pacing_amount
        self.pacing_interval = pacing_interval

    def execute(self):
        """
        rule:
            pacing_amount, pacing_interval
            if undefined in DB, follow POST logic
        """

        postValidator = PacingTypeRule(pacing_type=self.pacing_type,
                                       pacing_interval=self.pacing_interval,
                                       pacing_amount=self.pacing_amount)

        return postValidator.execute()
