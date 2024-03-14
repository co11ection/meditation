from django.urls import path
from .views import DataForAppListAPIView


urlpatterns = [
    path("data/", DataForAppListAPIView.as_view(), name="data-list"),
]
