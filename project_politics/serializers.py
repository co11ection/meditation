from rest_framework import serializers
from .models import ProjectConfidential, ProjectInfo, ProjectPolitic


class ProjectInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectInfo
        fields = ["text"]


class ProjectPoliticSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectPolitic
        fields = ["text"]


class ProjectConfidentialSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectConfidential
        fields = ["text"]
