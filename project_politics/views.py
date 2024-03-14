from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import ProjectConfidential, ProjectInfo, ProjectPolitic
from .serializers import (
    ProjectConfidentialSerializers,
    ProjectInfoSerializers,
    ProjectPoliticSerializers,
)


class ProjectInfoList(generics.ListAPIView):
    """
    Представление, отображающее список объектов ProjectInfo.

    Атрибуты класса:
        queryset: queryset для выборки всех объектов ProjectInfo.
        serializer_class: сериализатор для объектов ProjectInfo.
    """

    permission_classes = [AllowAny]
    queryset = ProjectInfo.objects.all()
    serializer_class = ProjectInfoSerializers


class ProjectPoliticList(generics.ListAPIView):
    """
    Представление, отображающее список объектов ProjectPolitic.

    Атрибуты класса:
        queryset: queryset для выборки всех объектов ProjectPolitic.
        serializer_class: сериализатор для объектов ProjectPolitic.
    """

    permission_classes = [AllowAny]
    queryset = ProjectPolitic.objects.all()
    serializer_class = ProjectPoliticSerializers


class ProjectConfidentialList(generics.ListAPIView):
    """
    Представление, отображающее список объектов ProjectConfidential.

    Атрибуты класса:
        queryset: queryset для выборки всех объектов ProjectConfidential.
        serializer_class: сериализатор для объектов ProjectConfidential.
    """

    permission_classes = [AllowAny]
    queryset = ProjectConfidential.objects.all()
    serializer_class = ProjectConfidentialSerializers


@api_view(["GET"])
@permission_classes([AllowAny])
def project_info_view(request):
    project_info = ProjectInfo.objects.first()
    return render(request, "info.html", {"project_info": project_info})


@api_view(["GET"])
@permission_classes([AllowAny])
def project_politic_view(request):
    project_politic = ProjectPolitic.objects.first()
    return render(request, "politic.html", {"project_politic": project_politic})


@api_view(["GET"])
@permission_classes([AllowAny])
def project_confidential_view(request):
    project_confidential = ProjectConfidential.objects.first()
    return render(
        request, "confidential.html", {"project_confidential": project_confidential}
    )
