""" REST views for the template API
"""
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.commons import exceptions as exceptions
from core_main_app.utils.file import get_file_http_response
from core_main_app.components.template import api as main_template_api


class TemplateDownload(APIView):
    """Download a Template"""

    def get_object(self, pk, request):
        """Get Template from db

        Args:

            pk: ObjectId
            request:

        Returns:

            Template
        """
        try:
            return main_template_api.get(pk, request=request)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Download the JSON Schema file from a Template

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: JSON Schema file
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            template_object = self.get_object(pk, request=request)

            return get_file_http_response(
                template_object.content,
                template_object.filename,
                "application/schema+json",
                ".schema.json",
            )
        except Http404:
            content = {"message": "Template not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
