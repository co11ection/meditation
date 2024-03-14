from django.urls import path, include, re_path
from rest_framework import routers
from .views import RoomViewSet, MessageViewSet
from . import consumers

# Создаем router для DRF viewsets
router = routers.DefaultRouter()
router.register("rooms", RoomViewSet)
router.register("messages", MessageViewSet)


# URL-паттерны для API
urlpatterns = [
    path("", include(router.urls)),
]
