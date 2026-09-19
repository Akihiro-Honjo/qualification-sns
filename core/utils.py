from datetime import date, timedelta

from studies.models import StudyRecord


# def get_streak(user):

#     today = date.today()

#     study_dates = set(
#         StudyRecord.objects.filter(
#             qualification__user=user
#         )
#         .values_list(
#             "study_date",
#             flat=True
#         )
#         .distinct()
#     )

#     # 今日勉強している場合は今日から確認
#     if today in study_dates:
#         check_day = today

#     # 今日まだ勉強していなければ昨日から確認
#     elif today - timedelta(days=1) in study_dates:
#         check_day = today - timedelta(days=1)

#     # 今日も昨日も勉強していなければ0日
#     else:
#         return 0

#     streak = 0

#     while check_day in study_dates:

#         streak += 1

#         check_day -= timedelta(days=1)

#     return streak

def get_streak(user, qualification=None):

    today = date.today()

    records = StudyRecord.objects.filter(
        qualification__user=user
    )

    if qualification is not None:
        records = records.filter(
            qualification=qualification
        )

    study_dates = set(
        records.values_list(
            "study_date",
            flat=True
        ).distinct()
    )

    if today in study_dates:
        check_day = today

    elif today - timedelta(days=1) in study_dates:
        check_day = today - timedelta(days=1)

    else:
        return 0

    streak = 0

    while check_day in study_dates:
        streak += 1
        check_day -= timedelta(days=1)

    return streak