import os

from ts_t1_validator.validators.rules.amount_ranges import T1AmountRanges, StrategyFrequencyRanges, StrategyRanges, StrategyImpressionRanges, StrategyGoalRanges
from .abstract_validator import AbstractValidator
from .rules.bids_rule import BidsRule
from .rules.frequency_required_fields import FrequencyRequiredFieldsRule
from .rules.frequency_type import FrequencyTypeRule
from .rules.goal_type import GoalTypeRule
from .rules.impression_pacing_type import ImpressionPacingTypeRule
from .rules.media_type_rule import MediaTypeRule
from .rules.pacing_type import PacingTypeRule
from .rules.roi_target_rule import StrategyRoiTargetRule
from .rules.strategy_dates import StrategyDatesRule
from .rules.strategy_dates_required import StrategyDatesRequiredRule
from .rules.strategy_frequency_type_for_pg import StrategyFrequencyTypeForPGRule
from .rules.strategy_goal_types_for_pg import StrategyGoalTypesForPGRule
from .rules.strategy_required_fields_post import StrategyPostRequiredFieldsRule
from .rules.strategy_type_rule import StrategyTypeRule
from .rules.strategy_use_optimization_for_pg import StrategyUseOptimizationForPGRule
from .rules.t1_budget import T1BudgetRule
from .. import T1Service
from ..models.dto.campaign import CampaignDTO
from ..models.dto.strategy import StrategyDTO
from ..models.enums.goal_type import GoalTypeEnum
from ..models.enums.impression_pacing_type import ImpressionPacingTypeEnum


class StrategyPostValidator(AbstractValidator):
    def __init__(self, t1_service: T1Service):
        """
        strategy validation manager
        :param t1_service: T1Service
        """
        self.rules = list()
        self.errors = list()
        self.json_schema = os.path.dirname(os.path.abspath(__file__)) + "/strategy/schema/strategy_schema.json"
        self.t1_service = t1_service

    def build_rules_set(self, *args, **kwargs):
        """
        Build rules set
        """

        # remove previous rules
        self.rules = list()

        dto = StrategyDTO.fromDict(kwargs.get("dto", {}))
        campaign_dto = CampaignDTO.fromDict(kwargs.get("campaign_dto", {}))

        # case: at least one of the following is required: pacing_type, impression_pacing_type,
        # min_bid, max_bid, goal_value, frequency_optimization
        self.rules.append(StrategyPostRequiredFieldsRule(pacing_type=dto.pacing_type,
                                                         impression_pacing_type=dto.impression_pacing_type,
                                                         min_bid=dto.min_bid, max_bid=dto.max_bid,
                                                         goal_value=dto.goal_value,
                                                         roi_target=dto.roi_target,
                                                         frequency_optimization=dto.frequency_optimization))

        # budget should be converted based on currency code and not be greater than 9,999,999.99.00 in USD
        if dto.budget is not None:
            self.rules.append(T1BudgetRule(
                budget=dto.budget,
                currency=campaign_dto.currency_code,
                t1_service=self.t1_service))

        # media_type validation
        self.rules.append(MediaTypeRule(media_type=dto.media_type))

        # strategy_type validation
        self.rules.append(StrategyTypeRule(strategy_type=dto.strategy_type))

        # pg campaign custom rules
        if campaign_dto.is_programmatic_guaranteed:
            self.add_rule(StrategyGoalTypesForPGRule(goal_type=dto.goal_type))
            self.add_rule(StrategyFrequencyTypeForPGRule(frequency_type=dto.frequency_type))
            self.add_rule(StrategyUseOptimizationForPGRule(use_optimization=dto.use_optimization))

        # pacing_* validation
        self.rules.append(PacingTypeRule(pacing_type=dto.pacing_type,
                                         pacing_interval=dto.pacing_interval,
                                         pacing_amount=dto.pacing_amount))

        # impression_pacing_* validation
        self.rules.append(ImpressionPacingTypeRule(impression_pacing_type=dto.impression_pacing_type,
                                                   impression_pacing_amount=dto.impression_pacing_amount,
                                                   impression_pacing_interval=dto.impression_pacing_interval))

        # frequency_* validation
        self.rules.append(FrequencyTypeRule(frequency_optimization=dto.frequency_optimization,
                                            frequency_type=dto.frequency_type,
                                            frequency_amount=dto.frequency_amount,
                                            frequency_interval=dto.frequency_interval))

        # Strategy dates required validator
        self.rules.append(StrategyDatesRequiredRule(use_campaign_start_date=dto.use_campaign_start_date,
                                                    use_campaign_end_date=dto.use_campaign_end_date,
                                                    start_date=dto.start_date,
                                                    end_date=dto.end_date))

        # Strategy dates overlap validator
        self.rules.append(StrategyDatesRule(use_campaign_start_date=dto.use_campaign_start_date,
                                            use_campaign_end_date=dto.use_campaign_end_date,
                                            campaign_start_date=campaign_dto.start_date,
                                            campaign_end_date=campaign_dto.end_date,
                                            start_date=dto.start_date,
                                            end_date=dto.end_date,
                                            zone_name=campaign_dto.zone_name))

        self.rules.append(FrequencyRequiredFieldsRule(frequency_type=dto.frequency_type, frequency_optimization=dto.frequency_optimization,
                                                      frequency_interval=dto.frequency_interval, frequency_amount=dto.frequency_amount,
                                                      cap_fields={"frequency_optimization": "frequency_optimization",
                                                                  "frequency_type": "frequency_type",
                                                                  "frequency_amount": "frequency_amount",
                                                                  "frequency_interval": "frequency_interval"}))

        if dto.goal_type is not GoalTypeEnum.UNDEFINED:
            self.add_rule(GoalTypeRule(goal_type=dto.goal_type,
                                       goal_value=dto.goal_value))

        # roi_target rule
        self.rules.append(StrategyRoiTargetRule(goal_type=dto.goal_type, roi_target=dto.roi_target))

        self.rules.append(T1AmountRanges(
            type_ranges=StrategyRanges,
            amount=dto.pacing_amount,
            amount_field="pacing_amount"))

        if dto.impression_pacing_type is not ImpressionPacingTypeEnum.UNDEFINED:
            self.rules.append(T1AmountRanges(
                type_ranges=StrategyImpressionRanges,
                amount=dto.impression_pacing_amount,
                amount_field="impression_pacing_amount"))

        if dto.frequency_amount is not None:
            self.rules.append(T1AmountRanges(
                type_ranges=StrategyFrequencyRanges,
                amount=dto.frequency_amount,
                amount_field="frequency_amount"))

        # rule for goal field
        self.rules.append(T1AmountRanges(
            type_ranges=StrategyGoalRanges,
            amount=dto.goal_value,
            amount_field="goal_value"))

        # rule for min/max bids
        self.rules.append(BidsRule(
            min_bid=dto.min_bid,
            max_bid=dto.max_bid
        ))
