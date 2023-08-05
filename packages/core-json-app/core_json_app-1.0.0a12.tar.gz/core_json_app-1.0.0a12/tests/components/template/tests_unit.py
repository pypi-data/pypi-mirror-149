""" Unit Test Template
"""
from unittest.case import TestCase

from mock import patch

import core_json_app.components.template.api as template_api
from core_json_app.commons.exceptions import JSONError
from core_main_app.components.template.models import Template
from tests.test_utils import create_template, get_valid_schema, get_invalid_schema


class TestTemplateUpsert(TestCase):
    @patch.object(Template, "save")
    def test_template_upsert_valid_template(self, mock_save):
        # Arrange
        template = create_template(get_valid_schema())
        mock_save.return_value = template
        # Act # Assert
        result = template_api.upsert(template)
        self.assertEquals(template, result)

    def test_template_upsert_invalid_template_raises_error(self):
        # Act # Assert
        with self.assertRaises(JSONError):
            template_api.upsert(create_template(get_invalid_schema()))
