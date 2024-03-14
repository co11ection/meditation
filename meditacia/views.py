from datetime import timedelta
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import generics

from wallet.views import WalletTokensView
from .models import UserProfile, GroupMeditation
from .serializers import UserProfileSerializer
from .models import Meditation
from .serializers import MeditationSerializer, GroupMeditationSerializer
from .tasks import update_meditation_time_async


class UserProfileMediation(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user.id)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class MeditationsListView(ReadOnlyModelViewSet):
    queryset = Meditation.objects.order_by("-created_date")
    serializer_class = MeditationSerializer


class MeditationCreateView(generics.CreateAPIView):
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer
    permission_classes = [IsAuthenticated]


class StartMeditationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meditation_id):
        """
        Начинает сеанс медитации для пользователя.
        """
        meditation = get_object_or_404(Meditation, id=meditation_id)
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.last_meditation_date == timezone.now().date():
            return Response(
                {"message": "Вы уже медитировали сегодня."},
                status=status.HTTP_400_BAD_REQUEST
            )

        meditation.scheduled_datetime = timezone.now()
        meditation.end_time = meditation.scheduled_datetime + meditation.duration
        meditation.completed = False
        meditation.save()

        # end_meditation.apply_async((meditation.id,), eta=end_time)

        end_meditation_url = reverse("meditacia:end-meditation", args=[meditation.id])

        return Response(
            {"message": "Начало медитации", "end_meditation_url": end_meditation_url},
            status=status.HTTP_200_OK,
        )


class EndMeditationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meditation_id):
        """
        Прерывает или завершает сеанс медитации и показывает результаты.
        """
        meditation: Meditation
        meditation = get_object_or_404(Meditation, id=meditation_id)
        meditation.duration += timedelta(seconds=5)
        meditation.completed = True
        meditation.save()

        user_profile = UserProfile.objects.get(user=request.user)
        update_meditation_time_async.delay(
            user_id=user_profile.user.id,
            meditation_duration=meditation.duration
        )

        wallet_tokens_view = WalletTokensView()
        balance = wallet_tokens_view.calculate_individual_tokens_to_earn(request)
        return Response({"earned_tokens": balance}, status=status.HTTP_200_OK)


class GroupMeditationViewSet(viewsets.ModelViewSet):
    queryset = GroupMeditation.objects.all()
    serializer_class = GroupMeditationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["POST"])
    def join(self, request, pk=None):
        meditation = self.get_object()
        user = request.user

        if user not in meditation.participants.all():
            meditation.participants.add(user)
            meditation.save()
            return Response({"message": "Вы успешно присоединились к медитации."})
        else:
            return Response(
                {"message": "Вы уже присоединены к этой медитации."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["GET"])
    def upcoming_meditations(self, request):
        now = timezone.now()
        upcoming_meditations = GroupMeditation.objects.filter(start_datetime__gt=now)
        serializer = GroupMeditationSerializer(upcoming_meditations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def past_meditations(self, request):
        now = timezone.now()
        past_meditations = GroupMeditation.objects.filter(start_datetime__lt=now)
        serializer = GroupMeditationSerializer(past_meditations, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class StartGroupMeditationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meditation_id):
        meditation: GroupMeditation
        meditation = get_object_or_404(GroupMeditation, id=meditation_id)
        if not meditation:
            return Response({"message": "Медитация не найдена"}, status=404)
        meditation.scheduled_datetime = timezone.now()
        meditation.end_time = meditation.scheduled_datetime + meditation.duration
        meditation.completed = False
        meditation.save()

        end_group_meditation_url = reverse("meditacia:end-group-meditation", args=[meditation.id])

        return Response(
            {"message": "Начало групповой медитации", "end_group_meditation_url": end_group_meditation_url},
            status=status.HTTP_200_OK,
        )


class EndGroupMeditationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, meditation_id):
        meditation: GroupMeditation
        meditation = get_object_or_404(GroupMeditation, id=meditation_id)
        if not meditation:
            return Response({"message": "Медитация не найдена"}, status=404)

        meditation.completed = True
        meditation.save()
        wallet_tokens_view = WalletTokensView()
        balance = wallet_tokens_view.calculate_individual_tokens_to_earn(request)

        for participant in meditation.participants.all():
            update_meditation_time_async.delay(
                user_id=participant.id,
                meditation_duration=meditation.duration,
                group_meditation=True
            )

        return Response({"earned_tokens": balance}, status=status.HTTP_200_OK)
