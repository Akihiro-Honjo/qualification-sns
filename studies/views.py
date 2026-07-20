from django.shortcuts import get_object_or_404, render

from goals.models import Qualification
from .models import StudyRecord

from django.shortcuts import redirect

from .forms import StudyRecordForm
# Create your views here.

def study_record_list(request, qualification_id):

    qualification = get_object_or_404(
        Qualification,
        pk=qualification_id,
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
    

def study_record_create(request, qualification_id):

    qualification = get_object_or_404(
        Qualification,
        pk=qualification_id,
    )

    if request.method == "POST":

        form = StudyRecordForm(request.POST)

        if form.is_valid():

            record = form.save(commit=False)

            record.qualification = qualification

            record.save()

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
    

def study_record_update(request, pk):

    record = get_object_or_404(
        StudyRecord,
        pk=pk,
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