from django import forms
from .models import Examiner

class ExaminerForm(forms.ModelForm):
    class Meta:
        model = Examiner
        fields = ["name", "email"]
