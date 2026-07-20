from django.shortcuts import render
from .models import Qualification

from django.shortcuts import redirect
from .forms import QualificationForm


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from studies.models import StudyRecord
from datetime import date
# Create your views here.


def qualification_list(request):
    qualifications = Qualification.objects.all()

    for qualification in qualifications:

        total_minutes = sum(
            StudyRecord.objects.filter(
                qualification=qualification
            ).values_list(
                "study_time",
                flat=True
            )
        )

        qualification.total_minutes = total_minutes
        qualification.total_hours = round(total_minutes / 60, 1)

        if qualification.target_hours > 0:
            qualification.progress = min(
                int(
                    qualification.total_hours
                    / qualification.target_hours
                    * 100
                ),
                100,
            )
        else:
            qualification.progress = 0
            
        if qualification.progress < 30:
            qualification.progress_color = "bg-danger"
        elif qualification.progress < 70:
            qualification.progress_color = "bg-warning"
        else:
            qualification.progress_color = "bg-success"

        today = date.today()

        if qualification.exam_date:
            qualification.days_left = (
                qualification.exam_date - today
            ).days
        else:
            qualification.days_left = None
            
# 追加ここから
        if qualification.days_left is not None and qualification.days_left > 0:

            remaining_hours = max(
                qualification.target_hours - qualification.total_hours,
                0
            )

            qualification.remaining_hours = round(
                remaining_hours,
                1
            )

            qualification.hours_per_day = round(
                remaining_hours / qualification.days_left,
                2
            )

        else:

            qualification.remaining_hours = 0
            qualification.hours_per_day = 0
# 追加ここまで
        if qualification.hours_per_day <= 1:
            qualification.advice = "このペースなら無理なく目標達成できそうです！"

        elif qualification.hours_per_day <= 2:
            qualification.advice = "少し意識して毎日学習を続けましょう！"

        else:
            qualification.advice = "目標達成には学習時間を増やす必要があります！"

        context = {
            "qualifications": qualifications,
        
        
    }

    return render(
        request,
        "goals/qualification_list.html",
        context,
    )

def qualification_create(request):

    if request.method == "POST":

        form = QualificationForm(request.POST)

        if form.is_valid():

            qualification = form.save(commit=False)

            
            # qualification.user = request.user 【戻す】
            qualification.user = User.objects.first()

            qualification.save()

            return redirect("qualification_list")

    else:

        form = QualificationForm()

    return render(
        request,
        "goals/qualification_form.html",
        {
            "form": form,
        },
    )
    

def qualification_update(request, pk):

    qualification = get_object_or_404(
        Qualification,
        pk=pk,
    )

    if request.method == "POST":

        form = QualificationForm(
            request.POST,
            instance=qualification,
        )

        if form.is_valid():
            form.save()
            return redirect("qualification_list")

    else:

        form = QualificationForm(
            instance=qualification,
        )

    return render(
        request,
        "goals/qualification_form.html",
        {
            "form": form,
        },
    )
    

def qualification_delete(request, pk):

    qualification = get_object_or_404(
        Qualification,
        pk=pk,
    )

    if request.method == "POST":
        qualification.delete()
        return redirect("qualification_list")

    return render(
        request,
        "goals/qualification_confirm_delete.html",
        {
            "qualification": qualification,
        },
    )