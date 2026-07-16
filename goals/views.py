from django.shortcuts import render
from .models import Qualification

from django.shortcuts import redirect
from .forms import QualificationForm


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

def qualification_list(request):
    qualifications = Qualification.objects.all()

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