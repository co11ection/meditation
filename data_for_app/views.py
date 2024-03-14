from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import DataForApp
from .serializers import DataForAppSerializers


class DataForAppListAPIView(ListCreateAPIView):
    serializer_class = DataForAppSerializers

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = DataForApp.objects.all()

        if self.request.method == "GET":
            language = self.request.query_params.get("language")

            if language:
                queryset = DataForApp.objects.filter(language=language)

        return queryset
