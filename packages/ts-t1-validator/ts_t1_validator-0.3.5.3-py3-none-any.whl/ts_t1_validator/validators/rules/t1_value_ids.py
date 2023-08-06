from ts_t1_validator.validators.exceptions import ValidationException
from ts_t1_validator.validators.rules.abstract_rule import ValidationRule


class T1ValueIdsRule(ValidationRule):
    def __init__(self, value_ids, field_name):

        assert type(value_ids) is list or value_ids is None, "value_ids should be a list or None"
        assert type(field_name) is str, "field_name should be a str"

        self.value_ids = value_ids
        self.field_name = field_name

    def execute(self):
        """
        format of provided "ids" is something like: num,num,num

        :return:
        """
        # ignore whole rule if value_ids is None
        if self.value_ids is None:
            return

        # parse str of value_ids into a list
        for value_id in self.value_ids:
            if not (value_id.isdigit() and int(value_id) > 0):
                raise ValidationException("%s should have valid format, positive numbers separated by comma" % self.field_name)
