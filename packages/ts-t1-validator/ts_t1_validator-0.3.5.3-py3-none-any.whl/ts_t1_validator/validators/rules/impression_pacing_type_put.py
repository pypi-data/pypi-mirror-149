from typing import Optional, Union

from ts_t1_validator.utils import is_number
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.impression_pacing_type import ImpressionPacingTypeRule
from ts_t1_validator.models.enums.impression_pacing_type import ImpressionPacingTypeEnum
from ts_t1_validator.models.enums.pacing_interval import PacingIntervalEnum


class ImpressionPacingTypePutRule(ValidationRule):
    def __init__(self, impression_pacing_type: ImpressionPacingTypeEnum,
                 impression_pacing_amount: Optional[Union[int, float]],
                 impression_pacing_interval: PacingIntervalEnum):

        assert type(impression_pacing_type) is ImpressionPacingTypeEnum, "impression_pacing_type should be type of ImpressionPacingTypeEnum"
        assert type(impression_pacing_interval) is PacingIntervalEnum, "impression_pacing_interval should be type of PacingIntervalEnum"

        self.impression_pacing_type = impression_pacing_type
        self.impression_pacing_amount = impression_pacing_amount
        self.impression_pacing_interval = impression_pacing_interval

    def put(self, pacing_amount: int or float or None, pacing_interval: PacingIntervalEnum):
        """
        method to reset fields in case we update the model, there is the only case:
        1) user switches type to no-limit, in this case both, amount and interval should be switched to None

        :param pacing_amount: int or float or None
        :param pacing_interval: PacingIntervalEnum
        :return: self
        """

        if self.impression_pacing_type is ImpressionPacingTypeEnum.NO_LIMIT:
            self.impression_pacing_amount = pacing_amount
            self.impression_pacing_interval = pacing_interval

        if is_number(pacing_amount):
            self.impression_pacing_amount = int(pacing_amount)

        return self

    def execute(self):
        """
        rule:
        common logic should stay the same
        """

        validator = ImpressionPacingTypeRule(
            impression_pacing_type=self.impression_pacing_type,
            impression_pacing_amount=self.impression_pacing_amount,
            impression_pacing_interval=self.impression_pacing_interval)

        return validator.execute()
