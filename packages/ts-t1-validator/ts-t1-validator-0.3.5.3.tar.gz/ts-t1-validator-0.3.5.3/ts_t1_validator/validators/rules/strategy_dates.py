from typing import Optional

from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.dates_overlap import DatesOverlapRule


class StrategyDatesRule(ValidationRule):
    campaign_start_date: Optional[str]
    campaign_end_date: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    use_campaign_start_date: bool
    use_campaign_end_date: bool
    zone_name: str

    def __init__(self, use_campaign_start_date: bool, use_campaign_end_date: bool,
                 campaign_start_date: str, campaign_end_date: str,
                 start_date: Optional[str], end_date: Optional[str],
                 zone_name: str):
        self.use_campaign_start_date = use_campaign_start_date
        self.use_campaign_end_date = use_campaign_end_date
        self.campaign_start_date = campaign_start_date
        self.campaign_end_date = campaign_end_date
        self.start_date = start_date
        self.end_date = end_date
        self.zone_name = zone_name

    def execute(self):
        start_date = self.start_date
        end_date = self.end_date
        if self.use_campaign_start_date is True:
            start_date = self.campaign_start_date

        if self.use_campaign_end_date is True:
            end_date = self.campaign_end_date

        if start_date is not None and end_date is not None:
            DatesOverlapRule(start_date=start_date,
                             end_date=end_date,
                             zone_name=self.zone_name).execute()
