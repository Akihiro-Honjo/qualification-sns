from django.shortcuts import render
from .models import Qualification

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