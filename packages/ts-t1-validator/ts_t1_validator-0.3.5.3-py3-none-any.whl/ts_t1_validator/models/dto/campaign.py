from ts_t1_validator.models.enums.cap_type import CapTypeEnum
from ts_t1_validator.models.enums.frequency_interval import FrequencyIntervalEnum
from ts_t1_validator.models.enums.frequency_type import FrequencyTypeEnum
from ts_t1_validator.models.enums.goal_type import GoalTypeEnum


class CampaignDTO:
    def __init__(self, advertiser_id, campaign_name, is_programmatic_guaranteed, status,
                 spend_cap_automatic, spend_cap_type, spend_cap_amount,
                 zone_name, start_date, end_date, currency_code, budget,
                 goal_type, goal_value, frequency_optimization,
                 frequency_type, frequency_interval, frequency_amount, restrict_targeting_to_same_device_id, merit_pixel_id):

        self.advertiser_id = advertiser_id
        self.campaign_name = campaign_name
        self.is_programmatic_guaranteed = is_programmatic_guaranteed
        self.status = status
        self.spend_cap_automatic = spend_cap_automatic
        self.spend_cap_type = spend_cap_type
        self.spend_cap_amount = spend_cap_amount
        self.zone_name = zone_name
        self.start_date = start_date
        self.end_date = end_date
        self.currency_code = currency_code
        self.budget = budget
        self.goal_type = goal_type
        self.goal_value = goal_value
        self.frequency_optimization = frequency_optimization
        self.frequency_type = frequency_type
        self.frequency_interval = frequency_interval
        self.frequency_amount = frequency_amount
        self.restrict_targeting_to_same_device_id = restrict_targeting_to_same_device_id
        self.merit_pixel_id = merit_pixel_id

    @staticmethod
    def fromDict(user_data: dict):
        """
        transform user data into inner object
        :param user_data: dict
        :return:
        """
        return CampaignDTO(advertiser_id=user_data.get("advertiser_id"),
                           campaign_name=user_data.get("campaign_name"),
                           is_programmatic_guaranteed=user_data.get("is_programmatic_guaranteed"),
                           status=user_data.get("status"),
                           spend_cap_automatic=user_data.get("spend_cap_automatic"),
                           spend_cap_type=CapTypeEnum.set(user_data.get("spend_cap_type")),
                           spend_cap_amount=user_data.get("spend_cap_amount"),
                           zone_name=user_data.get("zone_name"),
                           start_date=user_data.get("start_date"),
                           end_date=user_data.get("end_date"),
                           currency_code=user_data.get("currency_code"),
                           budget=user_data.get("budget"),
                           goal_type=GoalTypeEnum.set(user_data.get("goal_type")),
                           goal_value=user_data.get("goal_value"),
                           frequency_optimization=user_data.get("frequency_optimization"),
                           frequency_type=FrequencyTypeEnum.set(user_data.get("frequency_type")),
                           frequency_interval=FrequencyIntervalEnum.set(user_data.get("frequency_interval")),
                           frequency_amount=user_data.get("frequency_amount"),
                           restrict_targeting_to_same_device_id=user_data.get("restrict_targeting_to_same_device_id"),
                           merit_pixel_id=user_data.get("merit_pixel_id"))
