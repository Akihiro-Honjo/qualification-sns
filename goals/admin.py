from django.contrib import admin

# Register your models here.

from .models import Qualification


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "exam_date",
        "target_hours",
        "target_score",
    )
    search_fields = ("name",)
    list_filter = ("exam_date",)