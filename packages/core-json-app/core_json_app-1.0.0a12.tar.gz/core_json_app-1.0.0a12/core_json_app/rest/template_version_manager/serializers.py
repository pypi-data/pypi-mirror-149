"""Serializers used throughout the Rest API
"""

from core_json_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.template.models import Template
from core_main_app.rest.template.serializers import TemplateSerializer


class CreateTemplateSerializer(TemplateSerializer):
    """
    Template Version Manager serializer
    """

    def create(self, validated_data):
        """
        Create and return a new `Template` instance, given the validated data.
        """
        # TODO: check user is properly set
        template_object = Template(
            filename=validated_data["filename"],
            content=validated_data["content"],
            user=str(self.context["request"].user.id),
        )
        template_version_manager_object = validated_data["template_version_manager"]

        # Create the template and its template version manager
        template_version_manager_api.insert(
            template_version_manager_object,
            template_object,
            request=self.context["request"],
        )

        return template_object

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "Template Version Manager should only be updated using specialized APIs."
        )
