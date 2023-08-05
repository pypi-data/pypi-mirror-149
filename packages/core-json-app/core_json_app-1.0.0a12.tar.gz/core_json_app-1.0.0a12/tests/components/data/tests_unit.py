""" Unit Test Data
"""
from unittest.case import TestCase

from mock import patch

import core_json_app.components.data.api as data_api
from core_json_app.commons.exceptions import JSONError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from tests.test_utils import create_data, create_template, get_valid_schema


class TestDataUpsert(TestCase):
    @patch.object(data_api, "_save")
    def test_data_upsert_valid_data(self, mock_save):
        # Arrange
        template = create_template(get_valid_schema())
        json_data = {"firstName": "John", "lastName": "Doe", "age": 21}
        data = create_data(template, user_id="3", title="title", content=json_data)
        mock_save.return_value = data
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act # Assert
        result = data_api.upsert(data, request=mock_request)
        self.assertEquals(data, result)

    def test_data_upsert_invalid_value_raises_error(self):
        # Arrange
        template = create_template(get_valid_schema())
        json_data = {"firstName": "John", "lastName": "Doe", "age": "John"}
        data = create_data(template, user_id="3", title="title", content=json_data)
        mock_user = create_mock_user("3")
        mock_request = create_mock_request(user=mock_user)
        # Act # Assert
        with self.assertRaises(JSONError):
            data_api.upsert(data, request=mock_request)
