# from django.contrib.auth.decorators import login_required
# from datetime import date, timedelta
# from django.db.models import Sum
# from django.shortcuts import render
# import json

# from goals.models import Qualification
# from studies.models import StudyRecord
# # Create your views here.

# # def home(request):
# #     return render(request, "core/home.html")

# @login_required
# def home(request):

#     today = date.today()

#     week_start = today - timedelta(days=today.weekday())

#     # qualifications = Qualification.objects.count()
#     qualifications = Qualification.objects.filter(
#     user=request.user
#     ).count()

#     # study_records = StudyRecord.objects.count()
#     study_records = StudyRecord.objects.filter(
#     qualification__user=request.user
#     ).count()

#     today_minutes = (
#         StudyRecord.objects.filter(
#             qualification__user=request.user,
#             study_date=today,
#         )
#         .values_list("study_time", flat=True)
#     )

#     today_total = sum(today_minutes)

#     week_minutes = (
#         StudyRecord.objects.filter(
#             qualification__user=request.user,
#             study_date__gte=week_start,
#         )
#         .values_list("study_time", flat=True)
#     )
    
#     week_total = sum(week_minutes)

#     recent_records = (
#         StudyRecord.objects
#         .filter(
#             qualification__user=request.user
#         )
#         .select_related("qualification")
#         .order_by("-study_date")[:5]
#     )
    
#     study_dates = list(
#         StudyRecord.objects.filter(
#             qualification__user=request.user
#         )
#         .values_list(
#             "study_date",
#             flat=True
#         )
#         .distinct()
#     )

#     study_dates = sorted(study_dates, reverse=True)

#     streak = 0

#     if study_dates:

#         if study_dates[0] == today:
#             check_day = today

#         elif study_dates[0] == today - timedelta(days=1):
#             check_day = today - timedelta(days=1)

#         else:
#             check_day = None

#         while check_day is not None and check_day in study_dates:
#             streak += 1
#             check_day -= timedelta(days=1)

#     today_studied = StudyRecord.objects.filter(
#         qualification__user=request.user,
#         study_date=today,
#     ).exists()


#     # 追加
#     labels = []
#     study_times = []

#     for i in range(6, -1, -1):

#         target_day = today - timedelta(days=i)

#         total = (
#             StudyRecord.objects.filter(
#                 qualification__user=request.user,
#                 study_date=target_day,
#             ).aggregate(
#                 Sum("study_time")
#             )["study_time__sum"]
#             or 0
#         )

#         labels.append(target_day.strftime("%m/%d"))
#         study_times.append(total)
#     # ここまで

#     context = {
#         "qualification_count": qualifications,
#         "study_record_count": study_records,
#         "today_total": today_total,
#         "week_total": week_total,
#         "recent_records": recent_records,
#         "chart_labels": json.dumps(labels),
#         "chart_data": json.dumps(study_times),
#         "streak": streak,
#         "today_studied": today_studied,
#     }

#     return render(
#         request,
#         "core/home.html",
#         context,
#     )



# # study_dates = sorted(study_dates, reverse=True)

# # streak = 0

# # if study_dates:

# #     today = date.today()

# #     if study_dates[0] == today:
# #         check_day = today

# #     elif study_dates[0] == today - timedelta(days=1):
# #         check_day = today - timedelta(days=1)

# #     else:
# #         check_day = None

# #     while check_day in study_dates:

# #         streak += 1

# #         check_day -= timedelta(days=1)
    
# #     today_studied = StudyRecord.objects.filter(
# #     study_date=date.today()
# # ).exists()

from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.db.models import Sum
from django.shortcuts import render
import json

from goals.models import Qualification
from studies.models import StudyRecord
from .utils import get_streak


@login_required
def home(request):

    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    # ==============================
    # 現在学習中の資格
    # ==============================

    active_qualification = (
        Qualification.objects
        .filter(
            user=request.user,
            is_active=True
        )
        .first()
    )

    # 初期値
    total_hours = 0
    progress = 0
    days_left = None
    remaining_hours = 0
    hours_per_day = 0

    # 現在学習中の資格がある場合
    if active_qualification:

        total_minutes = (
            StudyRecord.objects
            .filter(
                qualification=active_qualification
            )
            .aggregate(
                total=Sum("study_time")
            )["total"]
            or 0
        )

        total_hours = round(
            total_minutes / 60,
            1
        )

        # 進捗率
        if active_qualification.target_hours > 0:

            progress = min(
                int(
                    total_hours
                    / active_qualification.target_hours
                    * 100
                ),
                100
            )

        # 試験までの日数
        days_left = (
            active_qualification.exam_date
            - today
        ).days

        # 残り学習時間
        remaining_hours = max(
            round(
                active_qualification.target_hours
                - total_hours,
                1
            ),
            0
        )

        # 1日あたり必要な学習時間
        if days_left > 0:

            hours_per_day = round(
                remaining_hours
                / days_left,
                2
            )

    # ==============================
    # 今日の学習時間
    # ==============================

    today_total = (
        StudyRecord.objects
        .filter(
            qualification__user=request.user,
            study_date=today
        )
        .aggregate(
            total=Sum("study_time")
        )["total"]
        or 0
    )

    # ==============================
    # 今週の学習時間
    # ==============================

    week_total = (
        StudyRecord.objects
        .filter(
            qualification=active_qualification,
            study_date__gte=week_start
        )
        .aggregate(
            total=Sum("study_time")
        )["total"]
        or 0
    )

    # ==============================
    # 連続学習日数
    # ==============================

    streak = get_streak(
        request.user,
        active_qualification
    )

    today_studied = (
        StudyRecord.objects
        .filter(
            qualification=active_qualification,
            study_date=today
        )
        .exists()
    )

    # ==============================
    # 直近7日間グラフ
    # ==============================

    labels = []
    study_times = []

    for i in range(6, -1, -1):

        target_day = (
            today
            - timedelta(days=i)
        )

    total = (
        StudyRecord.objects
        .filter(
            qualification=active_qualification,
            study_date=target_day
        )
        .aggregate(
            total=Sum("study_time")
        )["total"]
        or 0
    )

    labels.append(
            target_day.strftime("%m/%d")
        )

    study_times.append(total)

    # ==============================
    # テンプレートへ渡すデータ
    # ==============================

    context = {

        "active_qualification":
            active_qualification,

        "total_hours":
            total_hours,

        "progress":
            progress,

        "days_left":
            days_left,

        "remaining_hours":
            remaining_hours,

        "hours_per_day":
            hours_per_day,

        "today_total":
            today_total,

        "week_total":
            week_total,

        "streak":
            streak,

        "today_studied":
            today_studied,

        "chart_labels":
            json.dumps(labels),

        "chart_data":
            json.dumps(study_times),
    }

    return render(
        request,
        "core/home.html",
        context,
    )