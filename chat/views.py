from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        room = self.get_object()
        messages = room.messages.order_by('created_at')
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    def perform_update(self, serializer):
        serializer.save(host=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
