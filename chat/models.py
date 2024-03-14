from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    current_users = models.ManyToManyField(
        User, related_name="current_rooms", blank=True
    )

    def __str__(self) -> str:
        return f"{self.name} {self.host}"


class Message(models.Model):
    room = models.ForeignKey(
        "chat.Room", on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def count_reactions(self):
        return self.reactions.values('reaction_type').annotate(
            count=models.Count('reaction_type')).order_by()

    def __str__(self) -> str:
        return f"Message({self.user} {self.room})"


class Reaction(models.Model):
    message = models.ForeignKey(Message, related_name='reactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self) -> str:
        return f"Reaction{self.message} {self.user} {self.reaction_type}"
