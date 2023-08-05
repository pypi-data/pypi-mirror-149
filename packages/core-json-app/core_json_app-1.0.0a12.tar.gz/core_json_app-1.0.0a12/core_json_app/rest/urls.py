""" Url router for the REST API
"""

from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from core_json_app.rest.data import views as data_views
from core_json_app.rest.template import views as template_views
from core_json_app.rest.template_version_manager import (
    views as template_version_manager_views,
)

urlpatterns = [
    re_path(
        r"^data/$", data_views.DataList.as_view(), name="core_json_app_rest_data_list"
    ),
    re_path(
        r"^data/query/$",
        data_views.ExecuteLocalQueryView.as_view(),
        name="core_explore_common_local_query",
    ),
    re_path(
        r"^data/download/(?P<pk>\w+)/$",
        data_views.DataDownload.as_view(),
        name="core_json_app_rest_data_download",
    ),
    re_path(
        r"^data/(?P<pk>\w+)/$",
        data_views.DataDetail.as_view(),
        name="core_json_app_rest_data_detail",
    ),
    re_path(
        r"^template/user/$",
        template_version_manager_views.UserTemplateList.as_view(),
        name="core_json_app_rest_user_template_list",
    ),
    re_path(
        r"^template/global/$",
        template_version_manager_views.UserTemplateList.as_view(),
        name="core_json_app_rest_global_template_list",
    ),
    re_path(
        r"^template/(?P<pk>\w+)/download/$",
        template_views.TemplateDownload.as_view(),
        name="core_main_app_rest_template_download",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
