from ts_t1_validator import T1Service
from ts_t1_validator.utils import is_int
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class T1AdvertiserRule(ValidationRule):
    def __init__(self, advertiser_id: int, t1_service: T1Service):
        self.advertiser_id = advertiser_id
        self.t1_service = t1_service

    def execute(self):
        """
        - Must have T1 permissions
        - Must be integer
        - Must be greater than 0
        :return:
        """
        # check for attribute type
        if not is_int(self.advertiser_id) or self.advertiser_id < 1:
            raise ValidationException("Invalid advertiser_id")

        # check for attribute permission
        if not self.t1_service.isValidAdvertiser(self.advertiser_id):
            raise ValidationException("Invalid advertiser_id")
