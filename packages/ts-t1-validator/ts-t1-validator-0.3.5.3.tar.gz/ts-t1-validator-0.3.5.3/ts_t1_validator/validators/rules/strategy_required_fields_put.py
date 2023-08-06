from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.strategy_required_fields_post import StrategyPostRequiredFieldsRule
from ts_t1_validator.models.enums.impression_pacing_type import ImpressionPacingTypeEnum
from ts_t1_validator.models.enums.pacing_type import PacingTypeEnum


class StrategyPutRequiredFieldsRule(ValidationRule):
    def __init__(self, pacing_type, impression_pacing_type, min_bid,
                 max_bid, goal_value, roi_target, frequency_optimization):
        assert type(pacing_type) is dict, "pacing_type should be dictionary type"
        assert type(pacing_type.get("db")) is PacingTypeEnum, "pacing_type['db'] should be PacingTypeEnum type"
        assert type(pacing_type.get("dto")) is PacingTypeEnum, "pacing_type['dto'] should be PacingTypeEnum type"

        assert type(impression_pacing_type) is dict, "impression_pacing_type should be dictionary type"
        assert type(impression_pacing_type.get(
            "db")) is ImpressionPacingTypeEnum, "impression_pacing_type['db'] should be ImpressionPacingTypeEnum type"
        assert type(impression_pacing_type.get(
            "dto")) is ImpressionPacingTypeEnum, "impression_pacing_type['dto'] should be ImpressionPacingTypeEnum type"

        assert type(min_bid) is dict, "min_bid should be dictionary type"
        assert type(max_bid) is dict, "max_bid should be dictionary type"
        assert type(goal_value) is dict, "goal_value should be dictionary type"
        assert type(roi_target) is dict, "roi_target should be dictionary type"
        assert type(frequency_optimization) is dict, "frequency_optimization should be dictionary type"

        self.pacing_type = pacing_type
        self.impression_pacing_type = impression_pacing_type
        self.min_bid = min_bid
        self.max_bid = max_bid
        self.goal_value = goal_value
        self.roi_target = roi_target
        self.frequency_optimization = frequency_optimization

    def execute(self):
        """
        check for required fields step by step
        :return:
        """

        """
        rule
            pacing_type, impression_pacing_type, min_bid, max_bid, goal_value, roi_target, frequency_optimization
            - if undefined in DB, follow POST logic
        """
        if self.__oneOfRequiredFieldUndefinedInDb():
            postValidation = StrategyPostRequiredFieldsRule(pacing_type=self.getUpdatedValue("pacing_type"),
                                                            impression_pacing_type=self.getUpdatedValue(
                                                                "impression_pacing_type"),
                                                            min_bid=self.getUpdatedValue("min_bid"),
                                                            max_bid=self.getUpdatedValue("max_bid"),
                                                            goal_value=self.getUpdatedValue("goal_value"),
                                                            roi_target=self.getUpdatedValue("roi_target"),
                                                            frequency_optimization=self.getUpdatedValue(
                                                                "frequency_optimization"))
            return postValidation.execute()

    def __oneOfRequiredFieldUndefinedInDb(self):
        """
        check that one of required fields is undefined
        :return:
        """
        return self.pacing_type["db"] is PacingTypeEnum.UNDEFINED or self.impression_pacing_type[
            "db"] is ImpressionPacingTypeEnum.UNDEFINED or self.min_bid["db"] is None or self.max_bid[
            "db"] or self.goal_value["db"] is None or self.roi_target["db"] is None or self.frequency_optimization["db"] is None
