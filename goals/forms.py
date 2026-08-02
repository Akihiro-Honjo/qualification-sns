from django import forms
from .models import Qualification


class QualificationForm(forms.ModelForm):

    class Meta:
        model = Qualification

        fields = [
            "name",
            "exam_date",
            "target_hours",
            "target_score",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "exam_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "target_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "target_score": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }