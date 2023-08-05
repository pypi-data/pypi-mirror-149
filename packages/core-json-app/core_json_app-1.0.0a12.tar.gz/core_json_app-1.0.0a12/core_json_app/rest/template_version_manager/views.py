""" REST views for the template version manager API
"""

from core_json_app.rest.template_version_manager.serializers import (
    CreateTemplateSerializer,
)
from core_main_app.rest.template_version_manager import views as main_rest_views
from core_main_app.rest.template_version_manager.serializers import (
    TemplateVersionManagerSerializer,
)


class UserTemplateList(main_rest_views.UserTemplateList):
    """Create a Template (linked to the user)"""

    serializer = TemplateVersionManagerSerializer
    create_serializer = CreateTemplateSerializer


class GlobalTemplateList(main_rest_views.GlobalTemplateList):
    """Create a Template (global schema)"""

    serializer = TemplateVersionManagerSerializer
    create_serializer = CreateTemplateSerializer
