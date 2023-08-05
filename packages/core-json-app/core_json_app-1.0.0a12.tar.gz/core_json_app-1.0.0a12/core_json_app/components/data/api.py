""" Data API
"""
import datetime

import pytz

import core_main_app.access_control.api
import core_main_app.components.workspace.access_control
from core_json_app.utils.json_utils import validate_json_data
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions


@access_control(core_main_app.access_control.api.can_request_write)
def upsert(data, request):
    """Save or update the data.

    Args:
        data:
        request:

    Returns:

    """
    if data.dict_content is None:
        raise exceptions.ApiError("Unable to save data: dict_content field is not set.")

    data.last_modification_date = datetime.datetime.now(pytz.utc)
    validate_json_data(data.dict_content, data.template.content)
    return _save(data)


def _save(data):
    """Save the data in database

    Args:
        data:

    Returns:

    """
    data.convert_to_file()
    return data.save()
