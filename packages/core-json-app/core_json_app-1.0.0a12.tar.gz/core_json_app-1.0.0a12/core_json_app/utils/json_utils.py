""" JSON utils
"""
import json

from jsonschema import validate, Draft7Validator

from core_json_app.commons.exceptions import JSONError


def validate_json_data(data, schema):
    """Validate JSON data against JSON schema

    Args:
        data: dict content
        schema: string content

    Returns:

    """
    try:
        validate(data, json.loads(schema))
    except Exception as e:
        raise JSONError(str(e))


def is_schema_valid(schema):
    """Validate JSON schema

    Args:
        schema: string content

    Returns:

    """
    try:
        Draft7Validator.check_schema(json.loads(schema))
    except Exception as e:
        raise JSONError(str(e))
