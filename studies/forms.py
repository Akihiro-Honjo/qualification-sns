from datetime import date

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
                    "min": 1,
                    "step": 5,
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "例：機械学習の教師あり学習について",
                }
            ),

            "understanding": forms.Select(
                choices=[
                    (1, "1 - ほとんど理解できなかった"),
                    (2, "2 - あまり理解できなかった"),
                    (3, "3 - だいたい理解できた"),
                    (4, "4 - よく理解できた"),
                    (5, "5 - 十分理解できた"),
                ],
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # 新規登録の場合だけ今日の日付を初期値にする
        if not self.instance.pk:
            self.fields["study_date"].initial = date.today()