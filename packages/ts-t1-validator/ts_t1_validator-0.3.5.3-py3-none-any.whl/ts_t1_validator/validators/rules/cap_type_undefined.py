from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.cap_type import CapTypeEnum


class CapTypeUndefinedRule(ValidationRule):
    def __init__(self, cap_type1, cap_type2):

        assert isinstance(cap_type1, CapTypeEnum)
        assert isinstance(cap_type2, CapTypeEnum)

        self.cap_type1 = cap_type1
        self.cap_type2 = cap_type2

    def execute(self):
        """
        rule:
            required if impression_cap_type is undefined (one or the other must be defined at a minimum)
        :return:
        """

        if self.cap_type1 is CapTypeEnum.UNDEFINED and self.cap_type2 is CapTypeEnum.UNDEFINED:
            raise ValidationException("At least one of t1_spend_cap_type or impression_cap_type is required")
