from django import forms

from .models import Project, Task


class DateInput(forms.DateInput):
    """HTML5 date input widget."""

    input_type = "date"


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "status", "start_date", "due_date"]
        widgets = {
            "start_date": DateInput(),
            "due_date": DateInput(),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "status", "priority", "due_date"]
        widgets = {
            "due_date": DateInput(),
        }
