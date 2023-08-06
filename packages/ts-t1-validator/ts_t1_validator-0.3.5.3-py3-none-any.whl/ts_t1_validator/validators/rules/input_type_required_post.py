from typing import Union

from ts_t1_validator.validators.rules.abstract_rule import ValidationRule
from ts_t1_validator.validators.rules.input_type_required import InputTypeRequiredRule
from ts_t1_validator.models.enums.input_type import InputTypeEnum


class InputTypeRequiredPostRule(ValidationRule):
    def __init__(self, cap_amount1: Union[int, float, None], cap_amount2: Union[int, float, None], input_type: InputTypeEnum):
        assert isinstance(cap_amount1, (int, float, type(None))), "cap_amount1 should be type float or None"
        assert isinstance(cap_amount2, (int, float, type(None))), "cap_amount2 should be type float or None"
        assert isinstance(input_type, InputTypeEnum), "input_type should be type of InputTypeEnum"

        self.cap_amount1 = cap_amount1
        self.cap_amount2 = cap_amount2
        self.input_type = input_type

    def execute(self):
        """
        rules:
            input_type is required if defined one of cap_amounts
        :return: None
        """

        if self.cap_amount1 is not None or self.cap_amount2 is not None:
            InputTypeRequiredRule(input_type=self.input_type).execute()
