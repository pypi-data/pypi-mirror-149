import os

from ts_t1_validator.validators.rules.amount_ranges import T1AmountRanges, CampaignRanges, StrategyFrequencyRanges
from ts_t1_validator.validators.rules.cap_required_fields import CapRequiredFieldsRule
from .abstract_validator import AbstractValidator
from .rules.cap_amount import CapAmountRule
from .rules.cap_automatic import CapAutomaticRule
from .rules.dates_overlap import DatesOverlapRule
from .rules.frequency_required_fields import FrequencyRequiredFieldsRule
from .rules.frequency_type import FrequencyTypeRule
from .rules.goal_type import GoalTypeRule
from .rules.programmatic_guaranteed_overrides import ProgrammaticGuaranteedOverridesRule
from .rules.t1_advertiser import T1AdvertiserRule
from .rules.t1_budget import T1BudgetRule
from .rules.t1_merit_pixel import T1MeritPixelRule
from .. import T1Service
from ..models.dto.campaign import CampaignDTO


class CampaignPostValidator(AbstractValidator):
    def __init__(self, t1_service: T1Service):
        """
        campaign validation manager
        :param t1_service: T1Service
        """
        self.rules = list()
        self.errors = list()
        self.json_schema = os.path.dirname(os.path.abspath(__file__)) + "/campaign/schema/campaign_schema.json"
        self.t1_service = t1_service

    def build_rules_set(self, *args, **kwargs):
        """
        Build rules set
        :param args: Dict
        :param kwargs: Dict
        """
        # remove previous rules
        self.rules = list()

        dto = CampaignDTO.fromDict(kwargs.get("dto", {}))

        # check for advertiser
        if dto.advertiser_id:
            self.rules.append(T1AdvertiserRule(
                advertiser_id=dto.advertiser_id,
                t1_service=self.t1_service))

        # start_date is later than end_date. Message "start_date must be earlier than end_date"
        # start_time is later than end_time. Message " start_time must be earlier than end_time"
        # start_date is in the past. Message "start_date must be in the future"
        # start_date & end_date should be in YYYY-MM-DDTHH:MM:SS format
        if dto.start_date is not None and dto.end_date is not None:
            self.rules.append(DatesOverlapRule(dto.start_date, dto.end_date, dto.zone_name))

        # budget should be converted based on currency code and not be greater than 9,999,999.99.00 in USD
        if dto.budget is not None:
            self.rules.append(T1BudgetRule(
                budget=dto.budget,
                currency=dto.currency_code,
                t1_service=self.t1_service))

        # goal_type should be one of ctr, vcr, viewability_rate, cpa, cpc, reach, roi, spend, vcpm
        # goal_value Must be > 0 and <= 9,999,999.9999 if goal_type in (ROI, CPA, CPC, Viewable
        # CPM, CPM Reach, CPM Spend)
        # goal_value Must be > 0 and <= 100 if goal_type in (CTR, Video Completion Rate (VCR), Viewability Rate (VR))
        if dto.goal_type is not None:
            self.add_rule(GoalTypeRule(goal_type=dto.goal_type,
                                       goal_value=dto.goal_value))

        # pg campaign override values
        if dto.is_programmatic_guaranteed:
            self.rules.append(ProgrammaticGuaranteedOverridesRule(spend_cap_automatic=dto.spend_cap_automatic,
                                                                  spend_cap_type=dto.spend_cap_type,
                                                                  spend_cap_amount=dto.spend_cap_amount,
                                                                  frequency_optimization=dto.frequency_optimization,
                                                                  frequency_type=dto.frequency_type,
                                                                  frequency_interval=dto.frequency_interval,
                                                                  frequency_amount=dto.frequency_amount,
                                                                  restrict_targeting_to_same_device_id=dto.restrict_targeting_to_same_device_id))

        # validate PMP only fields
        else:
            # if present at least one spend cap field, all other should exists as well
            self.rules.append(
                CapRequiredFieldsRule(cap_type=dto.spend_cap_type,
                                      cap_automatic=dto.spend_cap_automatic,
                                      cap_amount=dto.spend_cap_amount,
                                      cap_fields={"cap_automatic": "spend_cap_automatic",
                                                  "cap_type": "spend_cap_type",
                                                  "cap_amount": "spend_cap_amount"}))

            # require spend_cap_automatic if spend_cap_type is not no-limit
            self.rules.append(CapAutomaticRule(cap_type=dto.spend_cap_type,
                                               cap_automatic=dto.spend_cap_automatic,
                                               cap_fields={"cap_automatic": "spend_cap_automatic",
                                                           "cap_type": "spend_cap_type"}))

            # require spend_cap_amount if spend_cap_type is not no-limit and spend_cap_automatic = 0
            self.rules.append(CapAmountRule(
                cap_type=dto.spend_cap_type,
                cap_automatic=dto.spend_cap_automatic,
                cap_amount=dto.spend_cap_amount,
                cap_fields={"cap_automatic": "spend_cap_automatic",
                            "cap_type": "spend_cap_type",
                            "cap_amount": "spend_cap_amount"}))

            # spend_cap_amount should be float >= 1 and <= 9999999.99
            if dto.spend_cap_amount is not None:
                self.rules.append(T1AmountRanges(
                    type_ranges=CampaignRanges,
                    amount=dto.spend_cap_amount,
                    amount_field="spend_cap_amount"))

            # verify frequency fields
            self.rules.append(FrequencyTypeRule(frequency_optimization=dto.frequency_optimization,
                                                frequency_type=dto.frequency_type,
                                                frequency_amount=dto.frequency_amount,
                                                frequency_interval=dto.frequency_interval))

            self.rules.append(FrequencyRequiredFieldsRule(frequency_type=dto.frequency_type,
                                                          frequency_optimization=dto.frequency_optimization,
                                                          frequency_interval=dto.frequency_interval,
                                                          frequency_amount=dto.frequency_amount,
                                                          cap_fields={
                                                              "frequency_optimization": "frequency_optimization",
                                                              "frequency_type": "frequency_type",
                                                              "frequency_amount": "frequency_amount",
                                                              "frequency_interval": "frequency_interval"}))

            # frequency_amount should be type of float >= 1 and <= 9999999
            if dto.frequency_amount is not None:
                self.rules.append(T1AmountRanges(
                    type_ranges=StrategyFrequencyRanges,
                    amount=dto.frequency_amount,
                    amount_field="frequency_amount"))

            self.rules.append(T1MeritPixelRule(
                goal_type=dto.goal_type,
                merit_pixel_id=dto.merit_pixel_id,
                t1_service=self.t1_service))
