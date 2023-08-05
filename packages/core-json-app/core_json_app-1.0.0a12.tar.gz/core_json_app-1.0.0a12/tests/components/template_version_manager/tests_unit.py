""" Template Version Manager unit tests
"""
from unittest.case import TestCase

from django.core import exceptions as django_exceptions
from mock.mock import patch

from core_json_app.components.template_version_manager import api as version_manager_api
from core_main_app.commons.exceptions import ModelError
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from tests.test_utils import (
    create_template,
    get_valid_schema,
    create_template_version_manager,
    get_invalid_schema,
)


class TestTemplateVersionManagerInsert(TestCase):
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.save"
    )
    @patch("core_main_app.components.template.models.Template.save")
    def test_create_version_manager_returns_version_manager(
        self, mock_save_template, mock_save_template_version_manager
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        template = create_template(get_valid_schema())
        mock_save_template.return_value = template

        version_manager = create_template_version_manager()
        mock_save_template_version_manager.return_value = version_manager

        # Act
        result = version_manager_api.insert(
            version_manager, template, request=mock_request
        )

        # Assert
        self.assertIsInstance(result, TemplateVersionManager)

    @patch("core_main_app.components.template.models.Template.save")
    def test_create_version_manager_raises_exception_if_error_in_create_template(
        self, mock_save
    ):
        # Arrange
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        template = create_template(get_valid_schema())

        mock_version_manager = create_template_version_manager()
        mock_save.side_effect = django_exceptions.ValidationError("")

        # Act + Assert
        with self.assertRaises(django_exceptions.ValidationError):
            version_manager_api.insert(
                mock_version_manager, template, request=mock_request
            )

    @patch("core_main_app.components.template.models.Template.delete")
    @patch(
        "core_main_app.components.template_version_manager.models.TemplateVersionManager.save"
    )
    @patch("core_main_app.components.template.models.Template.save")
    def test_create_version_manager_raises_exception_if_error_in_create_version_manager(
        self, mock_save_template, mock_save_version_manager, mock_delete_template
    ):
        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        template = create_template(get_valid_schema())

        mock_save_template.return_value = template
        version_manager = create_template_version_manager()
        mock_save_version_manager.side_effect = django_exceptions.ValidationError("")
        mock_delete_template.return_value = None

        # Act + Assert
        with self.assertRaises(ModelError):
            version_manager_api.insert(version_manager, template, request=mock_request)
