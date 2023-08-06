from typing import Union, Optional

from ts_t1_validator.models.enums.frequency_interval import FrequencyIntervalEnum
from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum
from ts_t1_validator.models.enums.goal_type import GoalTypeEnum
from ts_t1_validator.models.enums.impression_pacing_interval import ImpressionPacingIntervalEnum
from ts_t1_validator.models.enums.impression_pacing_type import ImpressionPacingTypeEnum
from ts_t1_validator.models.enums.media_type import MediaTypeEnum
from ts_t1_validator.models.enums.pacing_interval import PacingIntervalEnum
from ts_t1_validator.models.enums.pacing_type import PacingTypeEnum
from ts_t1_validator.models.enums.strategy_type import StrategyTypeEnum


class StrategyDTO:
    campaign_id: int
    name: str
    status: bool
    media_type: str
    strategy_type: str
    use_campaign_start_date: bool
    use_campaign_end_date: bool
    start_date: str
    end_date: str
    budget: Optional[Union[int, float]]
    use_optimization: bool
    goal_type: str
    bid_price_is_media_only: bool
    cost_passthrough_cpm_enabled: bool
    cost_passthrough_percent_enabled: bool

    def __init__(self, campaign_id, name, status, media_type, strategy_type,
                 use_campaign_start_date, use_campaign_end_date,
                 start_date, end_date, budget,
                 pacing_amount, pacing_interval, pacing_type,
                 impression_pacing_amount, impression_pacing_type,
                 impression_pacing_interval, bid_price_is_media_only,
                 min_bid, max_bid,
                 frequency_type, frequency_amount, frequency_interval, frequency_optimization,
                 use_optimization,
                 goal_type, goal_value, roi_target, cost_passthrough_cpm_enabled,
                 cost_passthrough_percent_enabled):

        self.campaign_id = campaign_id
        self.name = name
        self.status = status
        self.media_type = media_type
        self.strategy_type = strategy_type
        self.use_campaign_start_date = use_campaign_start_date
        self.use_campaign_end_date = use_campaign_end_date
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.pacing_amount = pacing_amount
        self.pacing_interval = pacing_interval
        self.pacing_type = pacing_type
        self.impression_pacing_amount = impression_pacing_amount
        self.impression_pacing_interval = impression_pacing_interval
        self.impression_pacing_type = impression_pacing_type
        self.bid_price_is_media_only = bid_price_is_media_only
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.frequency_type = frequency_type
        self.frequency_amount = frequency_amount
        self.frequency_interval = frequency_interval
        self.frequency_optimization = frequency_optimization
        self.use_optimization = use_optimization
        self.goal_type = goal_type
        self.goal_value = goal_value
        self.roi_target = roi_target
        self.cost_passthrough_cpm_enabled = cost_passthrough_cpm_enabled
        self.cost_passthrough_percent_enabled = cost_passthrough_percent_enabled

    @staticmethod
    def fromDict(user_data: dict):
        """
        transform user data into inner object
        :param user_data: dict
        :return:
        """
        return StrategyDTO(campaign_id=user_data.get("campaign_id"),
                           name=user_data.get("name"),
                           status=user_data.get("status"),
                           media_type=MediaTypeEnum.set(user_data.get("media_type")),
                           strategy_type=StrategyTypeEnum.set(user_data.get("strategy_type")),
                           use_campaign_start_date=user_data.get("use_campaign_start_date"),
                           use_campaign_end_date=user_data.get("use_campaign_end_date"),
                           start_date=user_data.get("start_date"),
                           end_date=user_data.get("end_date"),
                           budget=user_data.get("budget"),
                           pacing_amount=user_data.get("pacing_amount"),
                           pacing_interval=PacingIntervalEnum.set(user_data.get("pacing_interval")),
                           pacing_type=PacingTypeEnum.set(user_data.get("pacing_type")),
                           impression_pacing_amount=user_data.get("impression_pacing_amount"),
                           impression_pacing_type=ImpressionPacingTypeEnum.set(user_data.get("impression_pacing_type")),
                           impression_pacing_interval=ImpressionPacingIntervalEnum.set(user_data.get("impression_pacing_interval")),
                           bid_price_is_media_only=user_data.get("bid_price_is_media_only"),
                           min_bid=user_data.get("min_bid"),
                           max_bid=user_data.get("max_bid"),
                           frequency_type=FrequencyTypeEnum.set(user_data.get("frequency_type")),
                           frequency_amount=user_data.get("frequency_amount"),
                           frequency_interval=FrequencyIntervalEnum.set(user_data.get("frequency_interval")),
                           frequency_optimization=user_data.get("frequency_optimization"),
                           use_optimization=user_data.get("use_optimization"),
                           goal_type=GoalTypeEnum.set(user_data.get("goal_type")),
                           goal_value=user_data.get("goal_value"),
                           roi_target=user_data.get("roi_target"),
                           cost_passthrough_cpm_enabled=user_data.get("cost_passthrough_cpm_enabled"),
                           cost_passthrough_percent_enabled=user_data.get("cost_passthrough_percent_enabled"))
