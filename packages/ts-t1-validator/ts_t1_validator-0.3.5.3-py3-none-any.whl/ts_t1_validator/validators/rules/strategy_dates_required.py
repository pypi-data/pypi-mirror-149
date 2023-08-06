from typing import Optional

from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class StrategyDatesRequiredRule(ValidationRule):
    start_date: Optional[str]
    end_date: Optional[str]
    use_campaign_start_date: bool
    use_campaign_end_date: bool

    def __init__(self, use_campaign_start_date: bool, use_campaign_end_date: bool,
                 start_date: Optional[str], end_date: Optional[str]):
        self.use_campaign_start_date = use_campaign_start_date
        self.use_campaign_end_date = use_campaign_end_date
        self.start_date = start_date
        self.end_date = end_date

    def execute(self):
        if self.use_campaign_start_date is False and not self.start_date:
            raise ValidationException("start_date is required when use_campaign_start_date is False")

        if self.use_campaign_end_date is False and not self.end_date:
            raise ValidationException("end_date is required when use_campaign_end_date is False")
