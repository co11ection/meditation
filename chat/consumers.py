import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token
from .models import Room, Message, Reaction
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = await self.get_user_from_token(self.scope["path"].split("/")[-1])

        if self.user:
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'message':
            message = text_data_json["message"]
            avatar_url = await self.get_user_avatar_url(self.user)

            await self.save_message(message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "user_id": self.user.id,
                    "user_nickname": self.user.nickname,
                    "user_avatar": avatar_url,
                },
            )

            await self.send_notification(message)

        elif message_type == 'reaction':
            message_id = text_data_json["message_id"]
            reaction_type = text_data_json["reaction"]

            await self.save_reaction(message_id, reaction_type)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "reaction.message",
                    "message_id": message_id,
                    "user_id": self.user.id,
                    "reaction_type": reaction_type
                },
            )

    async def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        user_nickname = event["user_nickname"]
        user_avatar = event["user_avatar"]

        if self.user.id != user_id:
            await self.send(text_data=json.dumps({
                "message": message,
                "user_avatar": user_avatar,
                "user": user_nickname
            }))

    async def reaction_message(self, event):
        message_id = event["message_id"]
        reaction_type = event["reaction_type"]
        user_id = event["user_id"]

        await self.send(text_data=json.dumps({
            "message_id": message_id,
            "reaction_type": reaction_type,
            "user_id": user_id,
        }))

    async def chat_notification(self, event):
        message = event["message"]
        user_id = event["user_id"]
        user_nickname = event["user_nickname"]

        if self.user.id != user_id:
            await self.send(text_data=json.dumps({
                "message": message,
                "user": user_nickname,
                "notification": True},
                ensure_ascii=False
            ))

    async def send_notification(self, message):
        notification_data = {
            "type": "chat.notification",
            "message": "У вас новое сообщение: " + message,
            "user_id": self.user.id,
            "user_nickname": self.user.nickname,

        }

        await self.channel_layer.group_send(self.room_group_name, notification_data)

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            user = User.objects.get(id=token.user_id)
            return user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user_avatar_url(self, user):
        if user.photo:
            return user.photo.url
        return None

    @database_sync_to_async
    def save_message(self, message_text):
        if self.user:
            try:
                room = Room.objects.get(name=self.room_name)
            except Room.DoesNotExist:
                room = Room.objects.create(name=self.room_name, host=self.user)
            message = Message(room=room, text=message_text, user=self.user)
            message.save()

    @database_sync_to_async
    def save_reaction(self, message_id, reaction_type):
        message = Message.objects.get(id=message_id)
        reaction, created = Reaction.objects.get_or_create(
            message=message, user=self.user,
            defaults={'reaction_type': reaction_type}
        )
        if not created:
            reaction.reaction_type = reaction_type
            reaction.save()
