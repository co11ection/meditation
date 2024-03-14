from django.db import models


class ProjectInfo(models.Model):
    text = models.TextField(blank=True, null=True, verbose_name="О проекте")

    class Meta:
        managed = True
        db_table = "info"
        verbose_name_plural = "О проекте"


class ProjectPolitic(models.Model):
    text = models.TextField(blank=True, null=True, verbose_name="Политика соглашения")

    class Meta:
        managed = True
        db_table = "politic"
        verbose_name_plural = "Политика соглашения"


class ProjectConfidential(models.Model):
    text = models.TextField(
        blank=True, null=True, verbose_name="Политика конфиденциальности"
    )

    class Meta:
        managed = True
        db_table = "confidential"
        verbose_name_plural = "Политика конфиденциальности"
