from celery import shared_task
from datetime import timedelta
from .models import Meditation, GroupMeditation, UserProfile


@shared_task
def end_meditation(meditation_id):
    meditation = Meditation.objects.get(id=meditation_id)
    # Do whatever you need to do when the meditation ends,
    # such as calculating earned tokens, etc.
    if not meditation.completed:
        meditation.duration += timedelta(seconds=5)
        meditation.completed = True
    meditation.save()


@shared_task
def end_group_meditation(meditation_id):
    meditation = GroupMeditation.objects.get(id=meditation_id)
    if not meditation.completed:
        meditation.completed = True
    meditation.save()


@shared_task
def update_meditation_time_async(user_id, meditation_duration, group_meditation):
    user_profile = UserProfile.objects.get(user__id=user_id)
    user_profile.update_meditation_time(meditation_duration, group_meditation)
