from typing import Union

from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.cap_type import CapTypeEnum


class CapAutomaticPutRule(ValidationRule):
    def __init__(self, cap_type: CapTypeEnum, cap_automatic: bool or None,
                 cap_amount: Union[int, float, None], cap_fields=dict) -> None:
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
            1) it can defined alone as TRUE, only if t1_spend_cap_type in DB is asap or even.
            2) it can be defined alone as FALSE only if  DB's t1_spend_cap_amount is already defined.
            3) should be defined for even/asap
        :return:
        """

        # should be defined for even/asap
        if self.cap_automatic is None and self.cap_type in [CapTypeEnum.EVEN, CapTypeEnum.ASAP]:
            raise ValidationException(
                "For %(cap_type)s asap or even %(cap_automatic)s must be True or False" % self.cap_fields)

        # it can defined alone as TRUE, only if t1_spend_cap_type in DB is asap or even.
        if self.cap_automatic in [True, False] and self.cap_type not in [CapTypeEnum.EVEN, CapTypeEnum.ASAP]:
            self.cap_fields["cap_bool"] = str(self.cap_automatic)
            raise ValidationException(
                "For %(cap_automatic)s to be %(cap_bool)s, %(cap_type)s must be asap or even" % self.cap_fields)

        # it can be defined alone as FALSE only if  DB's t1_spend_cap_amount is already defined.
        if self.cap_automatic is False and self.cap_amount is None:
            raise ValidationException("Cannot define %(cap_automatic)s as False without %(cap_amount)s" % self.cap_fields)
