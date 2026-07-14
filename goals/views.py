from django.shortcuts import render
from .models import Qualification

from django.shortcuts import redirect
from .forms import QualificationForm


from django.contrib.auth.models import User
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

            
            # qualification.user = request.user
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