from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.cap_type import CapTypeEnum


class CapRequiredFieldsRule(ValidationRule):
    def __init__(self, cap_type, cap_automatic, cap_amount, cap_fields=dict):
        assert isinstance(cap_type, CapTypeEnum) or cap_type is None

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

    def execute(self):
        """
        rules:
            if present at least one field, cap_type should be defined as well
        :return:
        """

        if self.cap_amount is not None and self.cap_type is CapTypeEnum.UNDEFINED:
            raise ValidationException(
                "If you define %(cap_automatic)s, %(cap_amount)s you must define %(cap_type)s" % self.cap_fields)

        if self.cap_automatic is not None and self.cap_type is CapTypeEnum.UNDEFINED:
            raise ValidationException(
                "If you define %(cap_automatic)s, %(cap_amount)s you must define %(cap_type)s" % self.cap_fields)
