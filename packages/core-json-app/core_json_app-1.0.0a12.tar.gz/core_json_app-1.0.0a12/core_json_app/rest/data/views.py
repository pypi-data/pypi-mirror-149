""" REST views for the data API
"""
import json

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from core_json_app.rest.data import serializers as json_app_serializers
from core_main_app.commons import exceptions
from core_main_app.components.data import api as main_data_api
from core_main_app.rest.data import views as main_rest_views
from core_main_app.utils.file import get_file_http_response


class DataList(main_rest_views.DataList):
    """List all user Data, or create a new one."""

    permission_classes = (IsAuthenticated,)
    serializer = json_app_serializers.DataSerializer


class DataDetail(main_rest_views.DataDetail):
    """Retrieve, update or delete a Data"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer = json_app_serializers.DataSerializer


class DataDownload(APIView):
    """Download JSON file in data"""

    def get_object(self, request, pk):
        """Get Data from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return main_data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Download the JSON file from a data

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: JSON file
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object = self.get_object(request, pk)

            return get_file_http_response(
                json.dumps(data_object.dict_content),
                data_object.title,
                "application/json",
                "json",
            )
        except Http404:
            content = {"message": "Data not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExecuteLocalQueryView(main_rest_views.ExecuteLocalQueryView):
    serializer = json_app_serializers.DataSerializer
