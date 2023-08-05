""" Utils for Core Json App testing
"""
from bson import ObjectId

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)


def create_template_version_manager(title="schema.json", is_disabled=False, user_id=1):
    """Return a mock template version manager

    Args:
        title:
        is_disabled:
        user_id:

    Returns:

    """
    tvm = TemplateVersionManager(
        id=ObjectId(),
        title=title,
        versions=[],
        user=user_id,
        is_disabled=is_disabled,
        disabled_versions=[],
        _cls=TemplateVersionManager.class_name,
    )
    return tvm


def create_template(content):
    """Get template

    Returns:

    """
    template = Template()
    template.filename = "schema.json"
    template.content = content
    return template


def create_data(template, user_id, title, content):
    """Create mock data

    Args:
        template:
        user_id:
        title:
        content:

    Returns:

    """
    data = Data(template=template, user_id=user_id, title=title)
    data.dict_content = content
    return data


def get_invalid_schema():
    """Return JSON schema

    Returns:

    """
    return """{
      '$id': 'https://example.com/person.schema.json',
      '$schema': 'http://json-schema.org/draft-07/schema#',
    }"""


def get_valid_schema():
    """Return JSON schema

    Returns:

    """
    return """{
      "$id": "https://example.com/person.schema.json",
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "Person",
      "type": "object",
      "properties": {
        "firstName": {
          "type": "string",
          "description": "The person's first name."
        },
        "lastName": {
          "type": "string",
          "description": "The person's last name."
        },
        "age": {
          "description": "Age in years which must be equal to or greater than zero.",
          "type": "integer",
          "minimum": 0
        }
      }
    }"""


def get_valid_data():
    """Return valid JSON data

    Args:

    Returns:

    """
    return {"firstName": "John", "lastName": "Doe", "age": 21}


def get_invalid_data():
    """Return invalid JSON data

    Args:

    Returns:

    """
    return {"firstName": "John", "lastName": "Doe", "age": "John"}


def get_different_data():
    """Return JSON data for different schema

    Args:

    Returns:

    """
    return {
        "first": "John",
        "last": "Doe",
    }
