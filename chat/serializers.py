from rest_framework import serializers
from .models import Room, Message, Reaction


class ReactionSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source="user.nickname")

    class Meta:
        model = Reaction
        fields = ['reaction_type', 'user_nickname']


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user_nickname = serializers.ReadOnlyField(source="user.nickname", read_only=True)
    user_avatar = serializers.ImageField(source="user.photo")
    user_id = serializers.ReadOnlyField(source="user.id")
    reactions = ReactionSerializer(many=True, read_only=True)
    reactions_count = serializers.SerializerMethodField(
        method_name='get_reactions_count')

    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at_formatted', 'user_id', 'user_nickname',
                  'user_avatar', 'room', 'reactions', 'reactions_count']

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_reactions_count(self, obj):
        return obj.count_reactions()


class RoomSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source="host.nickname", read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["pk", "name", "host", "messages", "current_users", "last_message"]

    def get_last_message(self, obj: Room):
        last_msg = obj.messages.order_by("-created_at").first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None
