from django.contrib import admin

from .models import StudyRecord
# Register your models here.

@admin.register(StudyRecord)
class StudyRecordAdmin(admin.ModelAdmin):
    list_display = (
        "qualification",
        "study_date",
        "study_time",
        "understanding",
    )

    list_filter = (
        "study_date",
        "qualification",
    )

    search_fields = (
        "content",
        "memo",
    )