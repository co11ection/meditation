from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

app_name = "meditacia"

router = DefaultRouter()
router.register("meditation", views.MeditationsListView)
router.register("group_meditation", views.GroupMeditationViewSet)

urlpatterns = [
    path("profiles", views.UserProfileMediation.as_view(), name="profiles"),
    path("meditation-create/", views.MeditationCreateView.as_view(), name="meditation-create"),
    path(
        "start-meditation/<int:meditation_id>/",
        views.StartMeditationView.as_view(),
        name="start-meditation",
    ),
    path(
        "end-meditation/<int:meditation_id>/",
        views.EndMeditationView.as_view(),
        name="end-meditation",
    ),
    path(
        "start-group-meditation/<int:meditation_id>/",
        views.StartGroupMeditationView.as_view(),
        name="start-group-meditation",
    ),
    path(
        "end-group-meditation/<int:meditation_id>/",
        views.EndGroupMeditationView.as_view(),
        name="end-group-meditation",
    ),
    path("", include(router.urls)),
]
