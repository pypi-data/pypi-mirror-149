from .abstract_rule import ValidationRule
from ..exceptions import ValidationException


class T1CheckIds(ValidationRule):
    def __init__(self, include_value_ids, exclude_value_ids):

        self.include_value_ids = include_value_ids
        self.exclude_value_ids = exclude_value_ids

    def execute(self):
        if self.include_value_ids is None or self.exclude_value_ids is None:
            return

        intrsect = set(self.include_value_ids).intersection(self.exclude_value_ids)
        if len(intrsect) > 0:
            raise ValidationException("Cannot have the same value id in both exclude and include lists.")
