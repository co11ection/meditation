from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackListCreateView(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        user = self.request.user
        topic = self.request.data.get('topic')
        description = self.request.data.get('description')

        if user.is_authenticated and user.email:
            email = user.email
        else:
            email = self.request.data.get("email")

        feedback_instance = Feedback.objects.create(
            topic=topic,
            description=description,
            email_feedback=email,
        )

        return Response({'success': True, 'feedback': feedback_instance},
                        status=status.HTTP_201_CREATED)
