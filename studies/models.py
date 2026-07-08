from django.db import models

from goals.models import Qualification

# Create your models here.

class StudyRecord(models.Model):
    UNDERSTANDING_CHOICES = [
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ]

    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        related_name="study_records",
        verbose_name="資格"
    )

    study_date = models.DateField("学習日")

    study_time = models.PositiveIntegerField("学習時間（分）")

    content = models.TextField("学習内容")

    understanding = models.PositiveSmallIntegerField(
        "理解度",
        choices=UNDERSTANDING_CHOICES,
    )

    memo = models.TextField(
        "メモ",
        blank=True,
    )

    created_at = models.DateTimeField(
        "作成日時",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "更新日時",
        auto_now=True,
    )

    class Meta:
        verbose_name = "学習記録"
        verbose_name_plural = "学習記録"
        ordering = ["-study_date"]

    def __str__(self):
        return f"{self.qualification.name} - {self.study_date}"