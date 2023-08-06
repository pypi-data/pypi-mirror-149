from ts_t1_validator.utils import is_number
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from typing import Union, Optional

from ts_t1_validator.models.enums.cap_type import CapTypeEnum


class ImpressionCapTypeRule(ValidationRule):
    def __init__(self,
                 impression_cap_type: CapTypeEnum,
                 impression_cap_automatic: Optional[bool],
                 impression_cap_amount: Union[int, float, None]):

        assert isinstance(impression_cap_type, CapTypeEnum), "impression_cap_type should be CapTypeEnum type"
        assert isinstance(impression_cap_automatic, (bool, type(None))), "impression_cap_automatic should be bool type"
        assert isinstance(impression_cap_amount, (int, float, type(None))), \
            "impression_cap_amount should be int or float type"

        self.impression_cap_type = impression_cap_type
        self.impression_cap_automatic = impression_cap_automatic
        self.impression_cap_amount = impression_cap_amount

    def put(self, cap_automatic: bool, cap_amount: Union[int, float, None]):
        """
        method to reset fields in case we update the model, there are only 2 cases when we need to reset fields:
        1) user switches type to no-limit, in this case both, amount and automatic should be switched to None
        2) user set amount to True for cap_type ('asap', 'even'), in this case amount should be switched to None

        :param cap_automatic: bool
        :param cap_amount: float
        :return: self
        """

        if self.impression_cap_type is CapTypeEnum.NO_LIMIT:
            self.impression_cap_automatic = cap_automatic
            self.impression_cap_amount = cap_amount
        elif self.impression_cap_type in [CapTypeEnum.ASAP, CapTypeEnum.EVEN] and self.impression_cap_automatic is True:
            self.impression_cap_amount = cap_amount

        return self

    def execute(self) -> None:
        """
        Check for amount type, for fixed case it should be int, for percentage a float
        :return:
        """
        if self.impression_cap_type is CapTypeEnum.UNDEFINED:
            return

        if self.impression_cap_type in [CapTypeEnum.ASAP, CapTypeEnum.EVEN] and self.impression_cap_automatic is False:
            if not is_number(self.impression_cap_amount):
                raise ValidationException("impression_cap_amount must be a float")

        return
