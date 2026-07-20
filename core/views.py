from datetime import date, timedelta
from django.shortcuts import render

from goals.models import Qualification
from studies.models import StudyRecord
# Create your views here.

# def home(request):
#     return render(request, "core/home.html")

def home(request):

    today = date.today()

    week_start = today - timedelta(days=today.weekday())

    qualifications = Qualification.objects.count()

    study_records = StudyRecord.objects.count()

    today_minutes = (
        StudyRecord.objects.filter(
            study_date=today
        )
        .values_list("study_time", flat=True)
    )

    today_total = sum(today_minutes)

    week_minutes = (
        StudyRecord.objects.filter(
            study_date__gte=week_start
        )
        .values_list("study_time", flat=True)
    )

    week_total = sum(week_minutes)

    recent_records = (
        StudyRecord.objects
        .select_related("qualification")
        .order_by("-study_date")[:5]
    )

    context = {
        "qualification_count": qualifications,
        "study_record_count": study_records,
        "today_total": today_total,
        "week_total": week_total,
        "recent_records": recent_records,
    }

    return render(
        request,
        "core/home.html",
        context,
    )