import inspect
from jsonschema import ValidationError


class ValidationException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

        stack = inspect.stack()

        self.class_caller = stack[1][1]
        self.class_line = stack[1][2]


class JsonSchemaException(Exception):
    def __init__(self, ex):
        assert isinstance(ex, ValidationError)
        message = str(ex)

        # we need to replace standard errors with custom
        attr = "" if len(ex.path) < 1 else ex.path[0]
        if ex.validator in ["type", "enum", "format", "required"]:
            if ex.validator_value == "boolean":
                message = "'%s' value must be a boolean" % attr
            elif ex.validator_value == "integer":
                message = "'%s' value must be an integer" % attr
            elif ex.validator_value == "number":
                message = "'%s' value must be a float" % attr
            elif ex.validator == "enum":
                message = "'%s' value must be one of the following values ('%s')" % (attr, "','".join(ex.validator_value))
            elif ex.validator_value == "date":
                message = "'%s' value must be a date in YYYY-MM-DD format" % attr
            elif ex.validator_value == "time":
                message = "'%s' value must be a time in HH:MM:SS format" % attr
            elif ex.validator_value == "string":
                message = "'%s' value must be a string" % attr
            elif ex.validator == "type" and ex.validator_value == "array":
                message = "'%s' should have valid format, positive numbers separated by comma" % attr
            elif ex.validator == "required":
                message = str(ex.message)
            elif ex.validator_value == "email":
                message = "'{attr}' should contain valid email address"
        elif ex.validator == "minimum":
            message = "'{field_name}' must be greater than {min_value}".format(field_name=attr,
                                                                               min_value=ex.validator_value)
        elif ex.validator == "minLength":
            # definitely we need to check for non-empty values
            if len(ex.instance) < 1:
                message = f"'{attr}' is a mandatory field"
            else:
                message = "'{field_name}' is too short, must be from {min_value} to {max_value} characters long".format(field_name=attr,
                                                                                                                        min_value=ex.schema.get("minLength"),
                                                                                                                        max_value=ex.schema.get("maxLength"))
        elif ex.validator == "maxLength":
            # definitely we need to check for non-empty values
            if len(ex.instance) < 1:
                message = f"'{attr}' is a mandatory field"
            else:
                message = "'{field_name}' is too long, must be from {min_value} to {max_value} characters long".format(field_name=attr,
                                                                                                                       min_value=ex.schema.get("minLength"),
                                                                                                                       max_value=ex.schema.get("maxLength"))

        super().__init__(message)
