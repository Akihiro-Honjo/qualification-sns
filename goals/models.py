from django.conf import settings
from django.db import models

# Create your models here.

class Qualification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="qualifications"
    )
    name = models.CharField("資格名", max_length=100)
    exam_date = models.DateField("試験日")
    target_hours = models.PositiveIntegerField("目標勉強時間", default=0)
    target_score = models.PositiveIntegerField("目標点数", default=0)

    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "資格"
        verbose_name_plural = "資格"

    def __str__(self):
        return self.name