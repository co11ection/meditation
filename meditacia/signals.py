from django.contrib.auth import get_user_model

from users.models import CustomUser
from .models import Meditation, MeditationSession, UserProfile, GroupMeditation
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .tasks import end_meditation, end_group_meditation


@receiver(post_save, sender=MeditationSession)
def create_meditation_on_start(sender, instance, created, **kwargs):
    if created:
        Meditation.objects.create(
            name=f"Сеанс медитации {instance.start_time}",
            description="Описание медитации",
            duration=instance.meditation.duration,
            created_date=instance.start_time.date(),
        )


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
        )


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# @receiver(pre_save, sender=Meditation)
# def check_meditation_is_completed(sender, instance, **kwargs):
#     if Meditation.objects.filter(id=instance.id).exists():
#         if not instance.completed:
#             end_meditation.apply_async((instance.id,), eta=instance.end_time)
#
#
# @receiver(pre_save, sender=GroupMeditation)
# def check_group_meditation_is_completed(sender, instance, **kwargs):
#     if GroupMeditation.objects.filter(id=instance.id).exists():
#         if not instance.completed:
#             end_group_meditation.apply_async((instance.id,), eta=instance.end_time)
