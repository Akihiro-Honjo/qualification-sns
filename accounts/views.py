from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import SignUpForm
from goals.models import Qualification
from studies.models import StudyRecord
# Create your views here.

def signup(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = SignUpForm()

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form
        },
    )
    

# マイページ
@login_required
def profile(request):

    qualifications = Qualification.objects.filter(
        user=request.user
    )

    study_records = StudyRecord.objects.filter(
        qualification__user=request.user
    )

    # 登録資格数
    qualification_count = qualifications.count()

    # 総学習時間
    total_minutes = (
        study_records.aggregate(
            total=Sum("study_time")
        )["total"]
        or 0
    )

    total_hours = round(
        total_minutes / 60,
        1
    )

# 総学習日数
    study_days = (
        study_records
        .values("study_date")
        .distinct()
        .count()
    )

    context = {
        "qualification_count": qualification_count,
        "total_hours": total_hours,
        "study_days": study_days,
    }

    return render(
        request,
        "accounts/profile.html",
        context,
    )