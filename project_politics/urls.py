from django.urls import path, include
from . import views


urlpatterns = [
    path("get_info/", views.project_info_view, name="get_info"),
    path("get_politic/", views.project_politic_view, name="get_politic"),
    path("get_confidential/", views.project_confidential_view, name="get_confidential"),
    path("project_info/", views.ProjectInfoList.as_view(), name="project-info"),
    path(
        "project_politic/", views.ProjectPoliticList.as_view(), name="project-politic"
    ),
    path(
        "project_confidential/",
        views.ProjectConfidentialList.as_view(),
        name="project-confidential",
    ),
]
