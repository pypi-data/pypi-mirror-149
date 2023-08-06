from abc import ABC, abstractmethod
from typing import List, Dict
import json

from ts_t1_validator.validators.exceptions import ValidationException, JsonSchemaException
from jsonschema import ValidationError
from jsonschema.validators import Draft7Validator


class AbstractValidator(ABC):
    rules: list
    errors: list
    json_schema: str

    def _loadSchema(self, file_name):
        """
        load schema from json file
        :param file_name:
        :return: string
        """
        with open(file_name) as f:
            data = json.load(f)

        return data

    def jsonSchemaValidation(self, data) -> List:
        """
        run schema validation
        :param data:
        :return: List
        """
        errors = []
        try:
            # load main body
            schema = self._loadSchema(self.json_schema)

            # do primary validation
            v = Draft7Validator(schema)
            # errors = [x.absolute_path[0] + " : " + x.message for x in v.iter_errors(data)]

            for error in v.iter_errors(data):
                try:
                    raise JsonSchemaException(error)
                except JsonSchemaException as e:
                    errors.append(e)

            errors = [str(x) for x in errors]

        except ValidationError as e:
            errors.append(e.absolute_path[0] + " : " + e.message)

        return errors

    def add_rule(self, rule):
        """
        Append rule to common set
        :param rule:
        :return:
        """
        self.rules.append(rule)

    @abstractmethod
    def build_rules_set(self, *args, **kwargs):
        ...

    def validate(self, *args, **kwargs) -> List:
        """
        Run validation
        :return: List
        """
        self.errors = list()
        self.errors.extend(self.jsonSchemaValidation(kwargs.get("dto", {})))
        self.build_rules_set(*args, **kwargs)
        for rule in self.rules:
            try:
                rule.execute()
            except ValidationException as e:
                self.errors.append(str(e))

        return self.errors
