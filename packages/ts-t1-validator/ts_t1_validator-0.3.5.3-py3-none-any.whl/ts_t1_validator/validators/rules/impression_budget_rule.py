from .abstract_rule import ValidationRule
from ..exceptions import ValidationException


class ImpressionBudgetRule(ValidationRule):
    def __init__(self, impression_cap_automatic: bool or None, total_impression_budget: int or None):
        """
        As a user, I need to be prevented from scheduling a change to automatic campaign impression pacing cap,
        if my existing T1 campaign does not have a defined impression budget

        :param impression_cap_automatic: bool
        :param total_impression_budget: int|None
        """
        assert type(impression_cap_automatic) is bool or impression_cap_automatic is None, \
            "impression_cap_automatic should be bool or None"
        assert type(total_impression_budget) is int or total_impression_budget is None, \
            "total_impression_budget should be int or None"

        self.impression_cap_automatic = impression_cap_automatic
        self.total_impression_budget = total_impression_budget

    def execute(self):
        """
        rules:
        The T1 requirement is that you can only define campaigns.impression_cap_automatic as TRUE if there is
        a campaigns.total_impression_budget of >=1.
        Campaigns.total_impression_budget will never be 0, as T1 requires the value to be >=1.
        It can only be undefined or >=1.
        """

        if self.impression_cap_automatic is True:
            if self.total_impression_budget is None or self.total_impression_budget <= 1:
                raise ValidationException("Cannot set automatic daily impression cap if campaign does not have an impression budget defined")
