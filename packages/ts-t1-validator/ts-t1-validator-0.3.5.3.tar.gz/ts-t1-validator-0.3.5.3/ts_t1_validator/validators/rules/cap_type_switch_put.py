from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.cap_type import CapTypeEnum


class CapTypeSwitchPutRule(ValidationRule):
    def __init__(self, cap_type_new, cap_type_old, cap_fields=dict):

        assert type(cap_type_new) is CapTypeEnum, "cap_type_new should have type of CapTypeEnum"
        assert type(cap_type_old) is CapTypeEnum, "cap_type_new should have type of CapTypeEnum"

        self.cap_type_new = cap_type_new
        self.cap_type_old = cap_type_old
        self.cap_fields = cap_fields

    def execute(self):
        """
        rule:
            If the DB has asap it can be switched to even
            If the DB has even it can be switched to asap
        :return:
        """

        # If the DB has asap it can be switched to even
        if self.cap_type_old is CapTypeEnum.ASAP and self.cap_type_new not in [CapTypeEnum.EVEN, CapTypeEnum.ASAP]:
            raise ValidationException("%(cap_type)s cap_fields must be even" % self.cap_fields)

        # If the DB has even it can be switched to asap
        if self.cap_type_old is CapTypeEnum.EVEN and self.cap_type_new not in [CapTypeEnum.EVEN, CapTypeEnum.ASAP]:
            raise ValidationException("%(cap_type)s cap_fields must be even" % self.cap_fields)
