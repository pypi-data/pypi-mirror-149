from enum import Enum

from ts_t1_validator import T1Service
from ts_t1_validator.utils import is_int, is_number
from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class BudgetRanges(Enum):
    MIN_VALUE = 1
    MAX_VALUE = 9_999_999.99


class T1BudgetRule(ValidationRule):
    def __init__(self, budget: float, currency: str, t1_service: T1Service):
        self.budget = budget
        self.currency = currency
        self.t1_service = t1_service

    def execute(self):
        """
        - Must be a float
        - Must be >= 1 and <= 9,999,999.99.00 (in USD - convert from local currency to USD then check)
        :return:
        """
        # we have to ignore rule for invalid data
        if not is_number(self.budget) or not isinstance(self.currency, str):
            return

        self.currency = self.currency.lower()
        # do a conversion in case we receive non usd currency
        rate = 1
        if self.currency != "usd":
            try:
                rate = self.t1_service.getCurrencyRate(self.currency)
            except BaseException:
                ValidationException("Cannot get currency conversion rate")

        # check for ranges
        budget = rate * self.budget
        if BudgetRanges.MIN_VALUE.value > budget or budget > BudgetRanges.MAX_VALUE.value:
            raise ValidationException("budget is out of range")
