from datetime import date, timedelta
from django.db.models import Sum
from django.shortcuts import render
import json

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
    
    # 追加
    labels = []
    study_times = []

    for i in range(6, -1, -1):

        target_day = today - timedelta(days=i)

        total = (
            StudyRecord.objects.filter(
                study_date=target_day
            ).aggregate(
                Sum("study_time")
            )["study_time__sum"]
            or 0
        )

        labels.append(target_day.strftime("%m/%d"))
        study_times.append(total)
    # ここまで

    context = {
        "qualification_count": qualifications,
        "study_record_count": study_records,
        "today_total": today_total,
        "week_total": week_total,
        "recent_records": recent_records,
        "chart_labels": json.dumps(labels),
        "chart_data": json.dumps(study_times),
    }

    return render(
        request,
        "core/home.html",
        context,
    )