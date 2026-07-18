from django.shortcuts import get_object_or_404, render

from goals.models import Qualification
from .models import StudyRecord

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