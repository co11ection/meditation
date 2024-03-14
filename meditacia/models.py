from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    practice_time = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="Время практики"
    )
    daily_practice = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="Ежедневная практика"
    )
    continuous_practice = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="Непрерывная практика"
    )
    progress_accelerator = models.DecimalField(
        blank=True, null=True, decimal_places=2,
        max_digits=8, verbose_name="Ускоритель прогресса"
    )
    engaged_followers = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="Приглашенные подписчики"
    )
    last_meditation_date = models.DateField(
        blank=True, null=True, verbose_name="Дата последней медитации"
    )

    def invite_user(self):
        self.engaged_followers += 1
        self.save()

    def update_meditation_time(self, meditation_duration, group_meditation=False):
        today = timezone.now().date()
        meditation_duration_minutes = meditation_duration.total_seconds() / 60
        self.practice_time += meditation_duration_minutes

        if not group_meditation:
            self.daily_practice = meditation_duration_minutes

        if self.last_meditation_date == today - timezone.timedelta(days=1):
            self.continuous_practice += 1
        else:
            self.continuous_practice = 1

        self.last_meditation_date = today
        self.save()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Профиль Пользователя"
        verbose_name_plural = "Профиль Пользователя"


class Meditation(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название медитации")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    duration = models.DurationField(
        verbose_name="Длительность медитации", default=timedelta(minutes=3)
    )
    completed_by_users = models.ManyToManyField(
        "users.CustomUser", blank=True, related_name="completed_meditations"
    )
    created_date = models.DateField(verbose_name="Дата создания медитации", auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Медитация"
        verbose_name_plural = "Медитации"


class MeditationSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=[("active", "Active"), ("paused", "Paused")]
    )

    def __str__(self):
        return f"{self.user.nickname} - {self.meditation.name}"


class GroupMeditation(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_meditation",
        verbose_name="Автор",
    )
    name = models.CharField(max_length=200, verbose_name="Название медитации")
    participants = models.ManyToManyField(
        User, related_name="group_meditations", blank=True
    )
    start_datetime = models.DateTimeField(blank=True, null=True)
    group_size = models.PositiveIntegerField()
    duration = models.DurationField(verbose_name="Длительность медитации")
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Групповая медитация"
        verbose_name_plural = "Групповые медитации"
