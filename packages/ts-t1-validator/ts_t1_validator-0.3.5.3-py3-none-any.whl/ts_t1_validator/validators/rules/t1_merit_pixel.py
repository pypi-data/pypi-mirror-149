from ts_t1_validator import T1Service
from ts_t1_validator.models.enums.goal_type import GoalTypeEnum
from ts_t1_validator.utils import is_int
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class T1MeritPixelRule(ValidationRule):
    def __init__(self, goal_type: GoalTypeEnum, merit_pixel_id: int, t1_service: T1Service):
        self.goal_type = goal_type
        self.merit_pixel_id = merit_pixel_id
        self.t1_service = t1_service

    def execute(self):
        """
        - Must be integer
        - Must be greater than 0
        - Must be existent merit_pixel_id
        - required when goal_type is roi or cpa
        :return:
        """
        if self.goal_type in (GoalTypeEnum.ROI, GoalTypeEnum.CPA) and self.merit_pixel_id is None:
            raise ValidationException("merit_pixel_id is required when goal_type is roi or cpa")

        if self.goal_type not in (GoalTypeEnum.ROI, GoalTypeEnum.CPA) and self.merit_pixel_id is not None:
            raise ValidationException("merit_pixel_id should not be provided when goal_type is not roi or cpa")

        if self.merit_pixel_id is not None:
            # check for attribute type
            if not isinstance(self.merit_pixel_id, (int, float)):
                raise ValidationException("Invalid merit_pixel_id")
            if not is_int(self.merit_pixel_id):
                if self.merit_pixel_id - int(self.merit_pixel_id) > 0:
                    raise ValidationException("merit_pixel_id must be integer")

            merit_pixel_id = int(self.merit_pixel_id)

            if merit_pixel_id < 1:
                raise ValidationException("Invalid merit_pixel_id")

            # check for attribute permission
            if not self.t1_service.isValidMeritPixel(merit_pixel_id):
                raise ValidationException("Invalid merit_pixel_id")
