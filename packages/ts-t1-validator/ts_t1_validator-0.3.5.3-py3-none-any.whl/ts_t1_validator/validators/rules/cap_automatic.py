from .abstract_rule import ValidationRule
from ..exceptions import ValidationException
from ts_t1_validator.models.enums.cap_type import CapTypeEnum


class CapAutomaticRule(ValidationRule):
    def __init__(self, cap_type, cap_automatic, cap_fields=dict):
        assert isinstance(cap_type, CapTypeEnum)

        self.cap_type = cap_type
        self.cap_automatic = cap_automatic
        self.cap_fields = cap_fields

    def execute(self):
        """
        rules:
            1) must be undefined if "spend_cap_type" == "no-limit". This is because no-limit overrides this setting in T1
            2) required if "spend_cap_type" != "no-limit", but is defined
            3) must be undefined if spend_cap_type is undefined too
        :return:
        """

        if self.cap_type is CapTypeEnum.UNDEFINED or self.cap_type is None:
            raise ValidationException(
                "%(cap_type)s is required field" % self.cap_fields)

        if self.cap_type is CapTypeEnum.NO_LIMIT and self.cap_automatic is not None:
            raise ValidationException("%(cap_automatic)s must be undefined when %(cap_type)s is no-limit" % self.cap_fields)

        if self.cap_type in [CapTypeEnum.EVEN, CapTypeEnum.ASAP] and self.cap_automatic is None:
            raise ValidationException("%(cap_automatic)s is required when %(cap_type)s is asap or even" % self.cap_fields)
