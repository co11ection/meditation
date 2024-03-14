from django.db import models


class Feedback(models.Model):
    topic = models.CharField(max_length=100, verbose_name="Тема обращения")
    description = models.TextField(verbose_name="Обращение пользователя")
    email_feedback = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Почта для обратной связи"
    )
