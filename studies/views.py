from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from goals.models import Qualification

from .models import StudyRecord
from .forms import StudyRecordForm


@login_required
def study_record_list(request, qualification_id):

    qualification = get_object_or_404(
        Qualification,
        pk=qualification_id,
        user=request.user,
    )

    study_records = StudyRecord.objects.filter(
        qualification=qualification
    ).order_by("-study_date")

    context = {
        "qualification": qualification,
        "study_records": study_records,
    }

    return render(
        request,
        "studies/study_record_list.html",
        context,
    )


@login_required
def study_record_create(request, qualification_id):

    qualification = get_object_or_404(
        Qualification,
        pk=qualification_id,
        user=request.user,
    )

    if request.method == "POST":

        form = StudyRecordForm(request.POST)

        if form.is_valid():

            record = form.save(commit=False)

            record.qualification = qualification

            record.save()

            # 現在学習中の資格ならホームへ戻る
            if qualification.is_active:
                return redirect("home")

            # 過去・別資格なら資格別の学習記録一覧へ
            return redirect(
                "study_record_list",
                qualification_id=qualification.pk,
            )

    else:

        form = StudyRecordForm()

    return render(
        request,
        "studies/study_record_form.html",
        {
            "form": form,
            "qualification": qualification,
        },
    )


@login_required
def study_record_update(request, pk):

    record = get_object_or_404(
        StudyRecord,
        pk=pk,
        qualification__user=request.user,
    )

    if request.method == "POST":

        form = StudyRecordForm(
            request.POST,
            instance=record,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "study_record_list",
                qualification_id=record.qualification.pk,
            )

    else:

        form = StudyRecordForm(
            instance=record,
        )

    return render(
        request,
        "studies/study_record_form.html",
        {
            "form": form,
            "qualification": record.qualification,
        },
    )


@login_required
def study_record_delete(request, pk):

    record = get_object_or_404(
        StudyRecord,
        pk=pk,
        qualification__user=request.user,
    )

    qualification_id = record.qualification.pk

    if request.method == "POST":

        record.delete()

        return redirect(
            "study_record_list",
            qualification_id=qualification_id,
        )

    return render(
        request,
        "studies/study_record_confirm_delete.html",
        {
            "record": record,
        },
    )