from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.cap_type import CapTypeEnum


class CapAmountRule(ValidationRule):
    def __init__(self, cap_type, cap_automatic, cap_amount, cap_fields=dict):
        assert isinstance(cap_type, CapTypeEnum)

        self.cap_type = cap_type
        self.cap_amount = cap_amount
        self.cap_automatic = cap_automatic
        self.cap_fields = cap_fields

    def execute(self):
        """
        rules:
            1) must be undefined if "spend_cap_type" == "no-limit". This is because no-limit overrides this setting in T1
            2) must be undefined if "spend_cap_automatic == TRUE OR undefined, because it is meaningless otherwise
            3) required if "spend_cap_automatic == FALSE
            4) must be undefined if spend_cap_type is undefined too
        :return:
        """

        # must be undefined if spend_cap_type is undefined too
        if self.cap_type is CapTypeEnum.UNDEFINED:
            raise ValidationException(
                "%(cap_amount)s must be undefined when %(cap_type)s is not defined too" % self.cap_fields)

        # must be undefined if "spend_cap_type" == "no-limit". This is because no-limit overrides this setting in T1
        if self.cap_type is CapTypeEnum.NO_LIMIT and self.cap_amount is not None:
            raise ValidationException("%(cap_amount)s must be undefined when %(cap_type)s is no-limit" % self.cap_fields)

        # must be undefined if "spend_cap_automatic == TRUE OR undefined, because it is meaningless otherwise
        if self.cap_automatic is True and self.cap_amount is not None:
            raise ValidationException("%(cap_amount)s must be undefined when %(cap_automatic)s is TRUE" % self.cap_fields)

        # required if "spend_cap_automatic == FALSE
        if self.cap_automatic is False and self.cap_amount is None:
            raise ValidationException("%(cap_amount)s is required when %(cap_automatic)s is FALSE" % self.cap_fields)
