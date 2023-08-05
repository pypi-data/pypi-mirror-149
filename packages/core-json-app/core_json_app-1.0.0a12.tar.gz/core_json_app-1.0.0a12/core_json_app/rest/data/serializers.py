"""Serializers used throughout the data Rest API
"""

from django_mongoengine import fields
from rest_framework_mongoengine.serializers import DocumentSerializer

import core_json_app.components.data.api as data_api
from core_main_app.components.data.models import Data
from core_main_app.utils.xml import unparse


class DataSerializer(DocumentSerializer):
    """Data serializer"""

    class Meta(object):
        """Meta"""

        model = Data
        fields = [
            "id",
            "template",
            "workspace",
            "user_id",
            "title",
            "dict_content",
            "last_modification_date",
        ]
        read_only_fields = (
            "id",
            "user_id",
            "last_modification_date",
        )

    def create(self, validated_data):
        """
        Create and return a new `Data` instance, given the validated data.
        """
        # Create data
        instance = Data(
            dict_content=validated_data["dict_content"],
            template=validated_data["template"],
            workspace=validated_data["workspace"]
            if "workspace" in validated_data
            else None,
            title=validated_data["title"],
            user_id=str(self.context["request"].user.id),
        )
        # set xml content
        instance.xml_content = unparse(instance.dict_content, full_document=False)
        # Save the data
        data_api.upsert(instance, request=self.context["request"])

        return instance

    def update(self, instance, validated_data):
        """
        Update and return an existing `Data` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.dict_content = validated_data.get(
            "dict_content", instance.dict_content
        )
        return data_api.upsert(instance, request=self.context["request"])
