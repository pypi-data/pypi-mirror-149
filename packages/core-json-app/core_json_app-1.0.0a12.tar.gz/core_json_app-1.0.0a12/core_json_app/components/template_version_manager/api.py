"""
Template Version Manager API
"""
from core_json_app.components.template import api as template_api
from core_main_app.components.template import api as main_template_api
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.components.version_manager.utils import get_latest_version_name


# TODO: see how to refactor, everything except upsert is duplicated from main
def insert(template_version_manager, template, request):
    """Add a version to a template version manager.

    Args:
        template_version_manager:
        template:
        request:

    Returns:

    """
    # save the template in database
    template_api.upsert(template)
    try:
        # insert the initial template in the version manager
        version_manager_api.insert_version(
            template_version_manager, template, request=request
        )
        # insert the version manager in database
        version_manager_api.upsert(template_version_manager, request=request)
        # get template display name
        display_name = get_latest_version_name(template_version_manager)
        # update saved template
        main_template_api.set_display_name(template, display_name, request=request)
        # return version manager
        return template_version_manager
    except Exception as e:
        main_template_api.delete(template, request=request)
        raise e
