""" Unit Test JSON utils
"""
from unittest.case import TestCase

from core_json_app.commons.exceptions import JSONError
from core_json_app.utils.json_utils import is_schema_valid, validate_json_data
from tests.test_utils import (
    get_valid_schema,
    get_invalid_schema,
    get_invalid_data,
    get_different_data,
    get_valid_data,
)


class TestIsSchemaValid(TestCase):
    def test_is_schema_valid_with_valid_schema(self):
        is_schema_valid(get_valid_schema())

    def test_is_schema_valid_with_invalid_schema_raises_json_error(self):
        with self.assertRaises(JSONError):
            is_schema_valid(get_invalid_schema())


class TestValidateJsonData(TestCase):
    def test_validate_json_data_with_valid_data(self):
        validate_json_data(get_valid_data(), get_valid_schema())

    def test_validate_json_data_with_invalid_data(self):
        with self.assertRaises(JSONError):
            validate_json_data(get_invalid_data(), get_valid_schema())

    def test_validate_json_data_with_data_for_different_schema(self):
        # Schema doesn't require fields, completely different data is valid
        validate_json_data(get_different_data(), get_valid_schema())
