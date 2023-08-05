"""
Template API
"""
import hashlib
import logging

from core_json_app.utils.json_utils import is_schema_valid

logger = logging.getLogger(__name__)


def upsert(template):
    """Save or Updates the template.

    Args:
        template:

    Returns:

    """
    # Check if schema is valid
    is_schema_valid(template.content)
    # Get hash for the template
    # TODO: create proper hash function
    template.hash = hashlib.md5(template.content.encode("utf-8")).hexdigest()
    # Save template
    return template.save()
