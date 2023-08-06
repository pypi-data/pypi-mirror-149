import unittest

from faker import Faker

MANDATORY_MSG = "%s is required"


class CommonTestCase(unittest.TestCase):
    t1_service = None

    @classmethod
    def setUpClass(cls):
        cls._faker = Faker()

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def check_validator_error(self, *args, **kwargs):
        error = kwargs.get("validator").validate(**kwargs)
        if kwargs.get("expected_error") == "":
            self.assertEqual(len(error), 0, f"Validation error found: {error}")
        else:
            found_error = False
            for e in error:
                if kwargs.get("expected_error") in e:
                    found_error = True

            if found_error is False:
                self.fail(f"{kwargs.get('expected_error')} not found in list of errors")

    def check_rule_error(self, rule, expected_error):
        error = ""
        try:
            rule.execute()
        except Exception as e:
            error = e.args[0]

        self.assertTrue(expected_error in error)
