from django import forms
from .models import StudyRecord


class StudyRecordForm(forms.ModelForm):

    class Meta:
        model = StudyRecord

        fields = [
            "study_date",
            "study_time",
            "content",
            "understanding",
        ]

        widgets = {
            "study_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "study_time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "例：60",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "今日学習した内容を入力してください",
                }
            ),
            "understanding": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 5,
                }
            ),
        }