from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.cap_type import CapTypeEnum
from typing import Union, Optional


class CapAmountPutRule(ValidationRule):
    def __init__(self, cap_type: CapTypeEnum, cap_automatic: Optional[bool], cap_amount: Union[int, float, None],
                 cap_fields=dict):
        assert type(cap_type) is CapTypeEnum, "cap_type should be type of CapTypeEnum"
        assert type(cap_automatic) is bool or cap_automatic is None, "cap_automatic should be type of bool or None"
        assert isinstance(cap_amount, (int, float, type(None))), "cap_amount should be type of float or None"

        self.cap_type = cap_type
        self.cap_automatic = cap_automatic
        self.cap_amount = cap_amount
        self.cap_fields = cap_fields

    def put(self, cap_automatic: bool, cap_amount: float):
        """
        method to reset fields in case we update the model, there are only 2 cases when we need to reset fields:
        1) user switches type to no-limit, in this case both, amount and automatic should be switched to None
        2) user set amount to True for cap_type ('asap', 'even'), in this case amount should be switched to None

        :param cap_automatic: bool
        :param cap_amount: float
        :return: self
        """

        if self.cap_type is CapTypeEnum.NO_LIMIT:
            self.cap_automatic = cap_automatic
            self.cap_amount = cap_amount
        elif self.cap_type in [CapTypeEnum.ASAP, CapTypeEnum.EVEN] and self.cap_automatic is True:
            self.cap_amount = cap_amount

        return self

    def execute(self) -> None:
        """
        rules:
            1) cap_type in asap or even and cap_automatic is false -> cap_amount should not be None
            2) cap_type in asap or even and cap_automatic is true -> cap_amount should be undefined
            2) cap_type is no-limit -> cap_amount should be undefined
        :return:
        """

        # cap_type in asap or even and cap_automatic is false -> cap_amount should not be None
        if self.cap_type in [CapTypeEnum.EVEN, CapTypeEnum.ASAP] and self.cap_automatic is False and self.cap_amount is None:
            raise ValidationException(
                "When %(cap_type)s is even or asap and %(cap_automatic)s is false you must "
                "define %(cap_amount)s." % self.cap_fields)

        # cap_type in asap or even and cap_automatic is true -> cap_amount should be undefined
        if self.cap_type in [CapTypeEnum.EVEN, CapTypeEnum.ASAP] and self.cap_automatic is True and self.cap_amount is not None:
            raise ValidationException("When %(cap_type)s is even or asap and cap %(cap_automatic)s is "
                                      "true %(cap_amount)s must be undefined." % self.cap_fields)

        # cap_type is no-limit -> cap_amount should be undefined
        if self.cap_type is CapTypeEnum.NO_LIMIT and self.cap_amount is not None:
            raise ValidationException("When %(cap_type)s is no-limit %(cap_amount)s "
                                      "must be undefined." % self.cap_fields)
