from rest_framework.serializers import ModelSerializer
from .models import DataForApp


class DataForAppSerializers(ModelSerializer):
    class Meta:
        model = DataForApp
        fields = "__all__"
